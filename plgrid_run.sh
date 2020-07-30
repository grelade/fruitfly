#!/bin/bash -l
## fruitfly flow-hierarchy testrun
#SBATCH -A plgbionngan
##SBATCH -p plgrid
#SBATCH -p plgrid-testing


#SBATCH -N 2
#SBATCH --ntasks-per-node=1

#SBATCH --mem-per-cpu=100GB
#SBATCH --output="output.out"
#SBATCH --error="error.err"
##SBATCH --time=24:00:00 
#SBATCH --time=1:00:00 

cd $SLURM_SUBMIT_DIR
module load plgrid/tools/python/3.7
pip list | grep numpy
#python --version
python3.7 $1 
