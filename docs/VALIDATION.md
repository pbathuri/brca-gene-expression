# Package validation

Validation performed on 2026-10-14 UTC.

| Check | Result |
|---|---|
| Python numerical and data-contract tests | 17 passed (sports 5, fintech 6, biology 6) |
| Notebook schema | All 18 validated with nbformat |
| Notebook Python cells | All 18 ran successfully; fresh Python process per notebook |
| Demo sensitivity scripts | All 3 completed with seed 0 |
| Python compilation | All supplied Python files compiled |
| Shell/Slurm syntax | Checked with bash -n |
| ZIP integrity | Verified when packaged |

Jupyter kernel integration was attempted but this environment prohibits the local network interface used by the kernel. The cell-execution checks do not claim frontend/kernel integration passed. The included GitHub CI runs the actual nbclient workflow in a standard runner; no hosted CI run has occurred yet.

Real WRDS access, the French/GDC live acquisition scripts, R/DESeq2 installation and execution, actual Slurm submissions, and Tableau/Power BI workbooks were not executed here. They require the students' source access, software or institutional environment. The package contains ready-to-run adapters and instructions, not an assertion that those services were tested. Real biological inference deliberately fails without DESeq2 rather than substituting the demo test.

No remote GitHub repositories were created. The three independent repository folders and publish_repos.sh prepare that step. No real research data or research findings are bundled.

Test environment: Python 3.12.14. Recommended classroom/CI baseline: Python 3.11. Dependency ranges are supplied; create a lock after validating the classroom environment.

- numpy: 2.3.5
- pandas: 2.2.3
- scipy: 1.17.0
- matplotlib: 3.10.8
- scikit-learn: 1.8.0
- nbformat: 5.11.1
- nbclient: 0.11.0
