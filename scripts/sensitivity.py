from pathlib import Path
import sys,argparse,time,subprocess,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'src'))
import project as p
parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=0);parser.add_argument('--mode',choices=['demo','real'],default='demo');a=parser.parse_args()
out=root/'outputs'/a.mode/f'sensitivity_{a.seed}';out.mkdir(parents=True,exist_ok=True)
start=time.perf_counter()
threshold=[5,10,20,15,25][a.seed%5]
if a.mode=='real':
    subprocess.run(['Rscript',str(root/'scripts/deseq2.R'),str(root/'data/raw'),str(out),str(threshold)],check=True)
else:
    counts,meta,genes=p.load_data('demo')
    counts=counts.loc[(counts>=threshold).sum(axis=1)>=meta.patient.nunique()]
    p.differential((counts,meta,genes),out,mode='demo')
print('Count threshold:',threshold)
(out/'run.json').write_text(json.dumps({'seed':a.seed,'mode':a.mode,'wall_seconds':time.perf_counter()-start},indent=2))
print('Wrote',out)
