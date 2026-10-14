# Breast Cancer Gene Expression Analysis

**Question:** Which genes differ between primary breast tumors and adjacent normal tissue in matched TCGA-BRCA patients?

**Scope:** Open-access GDC STAR gene counts; paired patients with one primary tumor and one solid-tissue normal. Start with ten pairs; target all eligible pairs after QC. Use raw integer counts in DESeq2. Normal means adjacent tissue, not healthy volunteers.

## First run (Python 3.11)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_demo.py
jupyter lab
```
Windows PowerShell activation: `.venv\Scripts\Activate.ps1`. On macOS, Tableau is a practical choice; Power BI Desktop requires a supported Windows environment.

Open `notebooks/00_kickoff.ipynb`, then Week 1–5 in order. All Python notebook kernels use this environment. `PROJECT_MODE=demo` is the default and uses generated synthetic fixtures. Real mode reads files described in `docs/DATA.md`. To launch real mode on macOS/Linux:
```bash
PROJECT_MODE=real jupyter lab
```
PowerShell: `$env:PROJECT_MODE="real"; jupyter lab`. Never combine real and demo exports; each has its own output directory.

## Work agreement
Read `docs/ROADMAP.md` for milestones, `docs/TEAM.md` for owners and reviews, and `docs/AGENT_POLICY.md` before using a coding assistant. Start with `docs/KICKOFF.md` at the first Zoom call. The executive mentor owns scientific scope and acceptance decisions; students own implementation and explanations.

## Files you will use
- `notebooks/`: six working notebooks, with prompts for the team's decisions.
- `src/project.py`: tested baseline calculations; refactor small pieces here rather than copying cells.
- `docs/DATA.md`, `docs/METHODS.md`: contracts, acquisition and statistical choices.
- `docs/DELIVERY.md`: figures, dashboard or scientific presentation, and acceptance checklist.
- `hpc/`: parameterized Slurm examples; allocation and environment are configured locally.
- `tests/`: numerical and data-contract checks. Run `python -m unittest discover -s tests`.

Dependencies are bounded in `requirements.txt`, not claimed as a cross-platform lock. After the team confirms its environment, save `python -m pip freeze > environment.lock.txt`, record OS/Python, and use that file for reruns. Bioinformatics additionally records R sessionInfo. Do not put credentials or raw licensed data in Git.
