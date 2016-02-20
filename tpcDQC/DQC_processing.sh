#!/bin/bash

source /global/homes/r/reinhol1/.bashrc

cd /global/homes/r/reinhol1/work/captain/software/work-area/CAPTAIN/tpcDQC/
python tpcDQC_processing.py
python visualisation.py 
rsync -avzu -e "ssh -i /global/homes/r/reinhol1/.ssh/DQC_transfer" /global/project/projectdirs/captain/data/2016/tpcDQC/html/ captain@nngroup.physics.sunysb.edu:

#cronjob: 20 * * * * /global/homes/r/reinhol1/work/captain/software/work-area/CAPTAIN/tpcDQC/DQC_processing.sh