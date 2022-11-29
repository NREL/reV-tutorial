#!/bin/bash

#SBATCH --account=sample_allocation
#SBATCH --time=1:00:00
#SBATCH -o ./sample_submission.o
#SBATCH -e ./sample_submission.e
#SBATCH --job-name=sample_submission
#SBATCH --nodes=1
#SBATCH --mail-user=sample.email@email.gov
#SBATCH --mem=179000

echo Running on: $HOSTNAME, Machine Type: $MACHTYPE
source ~/.bashrc
source ~/.bash_conda
conda activate /path/to/your/sample/conda/environment/

reV -c /path/to/rev/pipeline.json pipeline --monitor
