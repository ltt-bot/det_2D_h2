#!/bin/bash
#SBATCH --job-name=graph_h2        # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1             # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --time=00:05:00          # total run time limit (HH:MM:SS)
#SBATCH --account=mueller

module load anaconda3/2024.6
conda activate det_outflow

srun python graph.py