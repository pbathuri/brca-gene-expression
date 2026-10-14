"""Acquire a deterministic paired TCGA-BRCA pilot from GDC open STAR counts."""
import argparse,hashlib,json,datetime
from pathlib import Path
import pandas as pd
import requests

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-pairs',type=int,default=10);a=ap.parse_args()
    if a.max_pairs<0:raise ValueError('Use zero for all pairs or a positive count')
    out=Path(__file__).resolve().parents[1]/'data/raw';out.mkdir(parents=True,exist_ok=True)
    if any((out/x).exists() for x in ['counts.csv','samples.csv','genes.csv']):raise FileExistsError('Archive existing cohort before re-acquisition')
    values={'cases.project.project_id':['TCGA-BRCA'],'data_type':['Gene Expression Quantification'],
            'analysis.workflow_type':['STAR - Counts'],'access':['open'],
            'cases.samples.sample_type':['Primary Tumor','Solid Tissue Normal']}
    filters={'op':'and','content':[{'op':'in','content':{'field':k,'value':v}} for k,v in values.items()]}
    fields='file_id,file_name,md5sum,cases.submitter_id,cases.samples.sample_id,cases.samples.submitter_id,cases.samples.sample_type'
    session=requests.Session();hits=[];offset=0
    while True:
        res=session.get('https://api.gdc.cancer.gov/files',params={'filters':json.dumps(filters),'fields':fields,'size':500,'from':offset},timeout=90)
        res.raise_for_status();data=res.json()['data'];batch=data['hits'];hits.extend(batch)
        offset+=len(batch)
        if offset>=data['pagination']['total']:break
        if not batch:raise RuntimeError('Pagination stopped early')
    (out/'gdc_query.json').write_text(json.dumps({'filters':filters,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hits':hits},indent=2))
    rows=[];ambiguous=[]
    for f in hits:
        candidates=[]
        for case in f.get('cases',[]):
            for s in case.get('samples',[]):
                if s.get('sample_type') in ['Primary Tumor','Solid Tissue Normal']:
                    candidates.append(dict(file_id=f['file_id'],file_name=f['file_name'],md5sum=f['md5sum'],patient=case['submitter_id'],
                    sample_id=s['submitter_id'],sample_type=s['sample_type'],condition='tumor' if s['sample_type']=='Primary Tumor' else 'normal'))
        if len(candidates)==1:rows+=candidates
        else:ambiguous.append(f['file_id'])
    x=pd.DataFrame(rows)
    if x.empty:raise RuntimeError('No unambiguous eligible files; review query metadata')
    x.to_csv(out/'candidates.csv',index=False)
    (out/'ambiguous_file_ids.json').write_text(json.dumps(ambiguous))
    eligible=x.groupby('patient').condition.agg(set);patients=sorted(eligible[eligible.map(lambda s:s=={'normal','tumor'})].index)
    if a.max_pairs:patients=patients[:a.max_pairs]
    selected=x[x.patient.isin(patients)].sort_values(['patient','condition','file_id']).drop_duplicates(['patient','condition'])
    if len(patients)<3:raise RuntimeError('Too few complete pairs')
    selected.to_csv(out/'gdc_manifest.csv',index=False)
    downloads=out/'gdc_counts';downloads.mkdir(exist_ok=True)
    series=[];annotations=None
    for row in selected.itertuples():
        path=downloads/(row.file_id+'.tsv')
        if not path.exists():
            res=session.get('https://api.gdc.cancer.gov/data/'+row.file_id,timeout=180);res.raise_for_status();path.write_bytes(res.content)
        if hashlib.md5(path.read_bytes()).hexdigest()!=row.md5sum:raise ValueError('Checksum mismatch: '+row.file_id)
        frame=pd.read_csv(path,sep='\t',comment='#')
        frame=frame[frame.gene_id.str.startswith('ENSG')].copy()
        frame['gene_id']=frame.gene_id.str.split('.').str[0]
        if frame.gene_id.duplicated().any():raise ValueError('Duplicate stable gene IDs')
        frame=frame.set_index('gene_id')
        counts=pd.to_numeric(frame['unstranded'],errors='raise').rename(row.sample_id)
        if annotations is None:annotations=frame[['gene_name','gene_type']]
        elif not counts.index.equals(annotations.index):raise ValueError('Gene annotation/order mismatch')
        series.append(counts)
        print('Downloaded and checked',row.sample_id)
    matrix=pd.concat(series,axis=1)
    matrix.to_csv(out/'counts.csv')
    selected.set_index('sample_id').loc[matrix.columns,['patient','condition','file_id','sample_type']].to_csv(out/'samples.csv')
    annotations.to_csv(out/'genes.csv')
    print('Complete pairs:',len(patients),'| Review cohort and annotation release before DESeq2')
if __name__=='__main__':main()
