#!/usr/bin/env bash
#SBATCH --job-name=dsc-sensitivity
#SBATCH --array=0-4%2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=logs/%x-%A_%a.out
set -euo pipefail
: "${PROJECT_ROOT:?Set PROJECT_ROOT}"
: "${VENV_PATH:?Set VENV_PATH}"
cd "$PROJECT_ROOT"
source "$VENV_PATH/bin/activate"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python scripts/sensitivity.py --seed "$SLURM_ARRAY_TASK_ID" --mode "${PROJECT_MODE:-demo}"
