"""Paired RNA-seq workflow. Real inference is delegated to DESeq2, never to the demo t-test."""
from pathlib import Path
import subprocess
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel,hypergeom
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def demo_data():
    rng=np.random.default_rng(43);n=12;g=500;cols=[];rows=[];arrays=[]
    baseline=rng.lognormal(4,1,g)
    for i in range(n):
        person=rng.lognormal(0,.2,g)
        for condition in ['normal','tumor']:
            sid=f'DEMO_{i:02}_{condition}';cols.append(sid);rows.append(dict(sample_id=sid,patient=f'DEMO_{i:02}',condition=condition))
            mean=baseline*person*rng.uniform(.7,1.3)
            if condition=='tumor':mean[:30]*=4;mean[30:60]/=4
            arrays.append(rng.negative_binomial(15,15/(15+mean)))
    counts=pd.DataFrame(np.array(arrays).T,index=[f'DEMO_G{i:04}' for i in range(g)],columns=cols).rename_axis('gene_id')
    meta=pd.DataFrame(rows).set_index('sample_id')
    genes=pd.DataFrame({'gene_id':counts.index,'gene_name':counts.index})
    return counts,meta,genes

def load_data(mode='demo'):
    if mode=='demo':return demo_data()
    if mode!='real':raise ValueError('mode must be demo or real')
    d=ROOT/'data/raw'
    return pd.read_csv(d/'counts.csv',index_col=0),pd.read_csv(d/'samples.csv',index_col=0),pd.read_csv(d/'genes.csv')

def preview(data):
    c,m,g=data;print(c.iloc[:5,:4]);print(m.head());print('genes, samples:',c.shape)

def validate(data):
    c,m,g=data
    assert c.index.is_unique and c.columns.is_unique and m.index.is_unique
    assert c.columns.equals(m.index), 'Sample order mismatch'
    a=c.to_numpy();assert np.isfinite(a).all() and (a>=0).all() and (a==np.floor(a)).all(), 'Raw nonnegative integer counts required'
    assert (c.sum()>0).all()
    assert m.condition.isin(['normal','tumor']).all()
    assert not m.duplicated(['patient','condition']).any()
    pairs=m.groupby('patient').condition.agg(set)
    assert all(x=={'normal','tumor'} for x in pairs), 'Incomplete pairs'
    assert len(pairs)>=3, 'Need biological replication'
    assert set(c.index)<=set(g.gene_id)
    return pd.DataFrame({'genes':[len(c)],'samples':[len(m)],'pairs':[len(pairs)]})

def log_cpm(data):
    c,_,_=data;return np.log2(c.div(c.sum(),axis=1)*1e6+1)

def qc(data,out):
    validate(data);c,m,_=data;out=Path(out);out.mkdir(parents=True,exist_ok=True)
    x=log_cpm(data);variable=x.var(axis=1).nlargest(min(500,len(x))).index
    model=PCA(n_components=2);pcs=model.fit_transform(x.loc[variable].T)
    frame=pd.DataFrame(pcs,index=m.index,columns=['PC1','PC2']).join(m)
    frame.to_csv(out/'pca_logcpm.csv');c.sum().rename('library_size').to_csv(out/'library_sizes.csv')
    fig,ax=plt.subplots(figsize=(6,5))
    for condition,group in frame.groupby('condition'):ax.scatter(group.PC1,group.PC2,label=condition)
    ax.legend();ax.set(title='Exploratory log-CPM PCA; real analysis also checks VST',xlabel=f'PC1 ({model.explained_variance_ratio_[0]:.1%})',ylabel=f'PC2 ({model.explained_variance_ratio_[1]:.1%})')
    fig.tight_layout();fig.savefig(out/'pca.png',dpi=150);plt.close(fig)
    return frame

def bh(p):
    p=np.asarray(p,float);out=np.full(len(p),np.nan);ok=np.isfinite(p);v=p[ok]
    if len(v)==0:return out
    order=np.argsort(v);ranked=v[order]*len(v)/np.arange(1,len(v)+1)
    adj=np.minimum.accumulate(ranked[::-1])[::-1].clip(0,1)
    restored=np.empty(len(v));restored[order]=adj;out[ok]=restored;return out

def differential(data,out,mode='demo'):
    validate(data);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    if mode=='real':
        subprocess.run(['Rscript',str(ROOT/'scripts/deseq2.R'),str(ROOT/'data/raw'),str(out)],check=True)
        return pd.read_csv(out/'differential_expression.csv')
    if mode!='demo':raise ValueError('Invalid mode')
    c,m,g=data;x=log_cpm(data)
    a=m[m.condition=='tumor'].sort_values('patient').index;b=m[m.condition=='normal'].sort_values('patient').index
    t,p=ttest_rel(x[a].to_numpy(),x[b].to_numpy(),axis=1)
    result=pd.DataFrame({'gene_id':c.index,'log2FoldChange':x[a].to_numpy().mean(1)-x[b].to_numpy().mean(1),
       'stat':t,'pvalue':p,'padj':bh(p),'method':'DEMO paired log-CPM t-test; NOT DESeq2'}).merge(g,on='gene_id',validate='one_to_one')
    result.to_csv(out/'differential_expression.csv',index=False);return result

def plots(result,data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(7,5));sig=(result.padj<.05)&(result.log2FoldChange.abs()>=1)
    ax.scatter(result.log2FoldChange,-np.log10(result.padj.clip(lower=1e-300)),c=np.where(sig,'#aa2140','#8a969f'),s=9)
    ax.set(xlabel='Tumor − normal log2 fold change',ylabel='−log10 adjusted p-value',title='Differential expression | '+('SYNTHETIC demonstration' if 'DEMO' in str(result.gene_id.iloc[0]) else 'TCGA-BRCA paired analysis'))
    fig.tight_layout();fig.savefig(out/'volcano.png',dpi=150);plt.close(fig)
    x=log_cpm(data);top=result.sort_values('padj').gene_id.head(30);x=x.loc[x.index.intersection(top)]
    z=x.sub(x.mean(axis=1),axis=0).div(x.std(axis=1).replace(0,np.nan),axis=0).fillna(0)
    fig,ax=plt.subplots(figsize=(10,6));im=ax.imshow(z,aspect='auto',cmap='RdBu_r',vmin=-2,vmax=2)
    ax.set(title='Top genes | row-standardized log-CPM; descriptive selection',xlabel='Samples in metadata order',ylabel='Genes');fig.colorbar(im,ax=ax,label='Row z score')
    fig.tight_layout();fig.savefig(out/'top_genes.png',dpi=150);plt.close(fig)

def enrich(result,gmt_path,out):
    # Ambiguous symbols are removed, rather than selecting the most significant row.
    usable=result.dropna(subset=['pvalue','padj','gene_name']).copy()
    usable=usable[~usable.gene_name.duplicated(keep=False)]
    universe=set(usable.gene_name.astype(str));sets={}
    for line in Path(gmt_path).read_text().splitlines():
        fields=line.split('\t')
        if len(fields)>=3:sets[fields[0]]=set(fields[2:])&universe
    rows=[]
    for direction in ['up','down']:
        hit=(usable.padj<.05)&((usable.log2FoldChange>=1) if direction=='up' else (usable.log2FoldChange<=-1))
        selected=set(usable.loc[hit,'gene_name'])
        for name,genes in sets.items():
            if not 15<=len(genes)<=500:continue
            k=len(selected&genes)
            rows.append(dict(direction=direction,pathway=name,overlap=k,set_size=len(genes),selected=len(selected),background=len(universe),pvalue=hypergeom.sf(k-1,len(universe),len(genes),len(selected)) if selected else 1.0))
    table=pd.DataFrame(rows,columns=['direction','pathway','overlap','set_size','selected','background','pvalue'])
    table['padj']=bh(table.pvalue.to_numpy()) # one correction across both directional families
    out=Path(out);out.mkdir(parents=True,exist_ok=True);table.to_csv(out/'pathways.csv',index=False)
    return table

def demo_gmt(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);p=out/'demo_sets.gmt'
    p.write_text('\n'.join(name+'\tSYNTHETIC\t'+'\t'.join(f'DEMO_G{i:04}' for i in genes) for name,genes in [('DEMO_SET_A',range(30)),('DEMO_SET_B',range(30,60)),('DEMO_SET_C',range(100,180))]))
    return p

def run_demo():
    data=load_data();out=ROOT/'outputs/demo';qc(data,out);res=differential(data,out);plots(res,data,out);enrich(res,demo_gmt(out),out)
    print('SYNTHETIC plumbing demo complete. Real inference requires DESeq2.')
