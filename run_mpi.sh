#!/bin/bash
#SBATCH --job-name=det_2D        # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=112             # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --time=01:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-user=jb5027@princeton.edu
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --account=mueller

module purge
module load openmpi/gcc/4.1.8

srun ./PeleC2d.gnu.MPI.ex det.inp