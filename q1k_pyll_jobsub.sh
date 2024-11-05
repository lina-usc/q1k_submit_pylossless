#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --account=def-emayada
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G

#source ~/eeg-env/bin/activate
#cd /project/def-emayada/q1k/pilot/q1k-external-pilot
source eeg-env/bin/activate
python main.py $@

