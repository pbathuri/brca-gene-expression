"""Execute demo notebooks in fresh kernels; fail immediately on cell errors."""
from pathlib import Path
import os
import nbformat
from nbclient import NotebookClient
root=Path(__file__).resolve().parents[1]
os.environ['PROJECT_MODE']='demo'
for path in sorted((root/'notebooks').glob('*.ipynb')):
    notebook=nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(notebook, timeout=600, kernel_name='python3', resources={'metadata':{'path':str(root)}}).execute()
    out=root/'outputs'/'demo'/'executed'; out.mkdir(parents=True,exist_ok=True)
    nbformat.write(notebook, out/path.name)
    print('PASS',path.name)
