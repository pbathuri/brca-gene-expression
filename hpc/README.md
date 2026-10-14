# IU compute workflow

The analysis is CPU-first. A GPU is not necessary for these baselines. Use the supercomputer to learn reproducible batch work and run independent sensitivity checks; benchmark against a laptop instead of assuming a speedup.

Ask the mentor to confirm your own account, approved allocation, partition and storage path. Do not copy an allocation from someone else's project. Consult IU's Slurm guide and Big Red 200 documentation linked in SOURCES.md. Cluster names, modules and queues can change.

1. Clone the repo on approved project/scratch storage. Keep source backed up; scratch is not permanent storage.
2. Create the Python environment once using a supported Python module or approved environment. Use `module avail`/site instructions; no unverified module name is hard-coded here. For biology also install R/Bioconductor as documented.
3. Transfer only permitted inputs and verify their SHA-256 hashes. Install packages and stage downloads before submitting; do not launch large network downloads inside compute jobs.
4. Make the log directory **before** sbatch, then submit:
```bash
mkdir -p logs
export PROJECT_ROOT="$PWD"
export VENV_PATH="$PWD/.venv"
export NOTEBOOK=notebooks/02_metrics_qc.ipynb
export PROJECT_MODE=demo
sbatch --account=YOUR_ALLOCATION --partition=YOUR_CPU_PARTITION hpc/notebook.sbatch
```
5. Monitor `squeue -u "$USER"`. Inspect logs. After completion, use `sacct -j JOB_ID --format=JobID,Elapsed,MaxRSS,State,ExitCode`. Record queue wait separately from runtime. Use `scancel JOB_ID` for a mistaken job.
6. Compare local and cluster outputs with tolerances; numerical libraries may differ slightly. Record commit, input hashes, environment, job ID, seed, wall time, CPU count and peak memory in `docs/RUN_LOG.csv`.

Use IU's approved interactive Jupyter service if available to your account. Otherwise work locally and batch-execute notebooks. Do not start an unauthenticated public Jupyter server on a login node. Heavy analysis belongs on compute nodes.

Start with 4 CPUs / 16 GB / 30 minutes. For full TCGA fitting, a starting request of 8 CPUs / 32 GB / 2 hours may be sensible; measure and adjust, not a guaranteed requirement. DESeq2 is serial here unless explicitly configured otherwise. Avoid requesting idle cores.

The sensitivity script runs independent seeds locally or in a job array. A fixed seed must reproduce the same result. Set array concurrency to at most two for the class exercise, and compare outputs before scaling up.
