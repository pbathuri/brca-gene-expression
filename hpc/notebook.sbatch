#!/usr/bin/env bash
#SBATCH --job-name=dsc-notebook
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x-%j.out
set -euo pipefail
: "${PROJECT_ROOT:?Set PROJECT_ROOT to your cloned repo}"
: "${VENV_PATH:?Set VENV_PATH to your installed Python environment}"
: "${NOTEBOOK:?Set NOTEBOOK to notebooks/NN_name.ipynb}"
cd "$PROJECT_ROOT"
source "$VENV_PATH/bin/activate"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export PROJECT_MODE=${PROJECT_MODE:-demo}
mkdir -p "outputs/$PROJECT_MODE/executed"
python -m jupyter nbconvert --to notebook --execute "$NOTEBOOK" --output-dir "outputs/$PROJECT_MODE/executed" --ExecutePreprocessor.timeout=3600
