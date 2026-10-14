"""Validate notebook schema and run Python cells in a fresh process per notebook.
This is not a Jupyter frontend/kernel integration test. Use execute_notebooks.py for that.
"""
from pathlib import Path
import os,subprocess,sys
import nbformat
root=Path(__file__).resolve().parents[1]
os.environ['PROJECT_MODE']='demo'
for path in sorted((root/'notebooks').glob('*.ipynb')):
    notebook=nbformat.read(path,as_version=4);nbformat.validate(notebook)
    code='\n\n'.join(c.source for c in notebook.cells if c.cell_type=='code')
    subprocess.run([sys.executable,'-c',code],cwd=root,check=True,stdout=subprocess.DEVNULL)
    print('PASS Python cells:',path.name)
