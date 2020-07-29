#!/bin/bash -l
## fruitfly flow-hierarchy testrun
#SBATCH -A plgbionngan
#SBATCH -p plgrid
#SBATCH --mem-per-cpu=100GB
#SBATCH --output="output.out"
#SBATCH --error="error.err"
#SBATCH --time=24:00:00 

export NEUPRINT_APPLICATION_CREDENTIALS=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphY2VrZ3JlbGFAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHaHVOYW9TVkhPMjdjVmtWYllPM3pwVHRzcTJKN3VSNXUtdTZMY05Idz9zej01MD9zej01MCIsImV4cCI6MTc2NDcyNzk3MX0.el15xSIKdGF52Hdrk1j-vrfm7QBMnBs0rzQCpjiVKg4
cd $SLURM_SUBMIT_DIR
module load plgrid/tools/python/3.7
pip list | grep numpy
#python --version
python3.7 plgrid_primary_roi_fh.py 
