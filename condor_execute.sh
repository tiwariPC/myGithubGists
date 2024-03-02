#!/bin/sh
ulimit -s unlimited
set -e
## full directory name is needed
cd <CMSSW base directory>
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd <CMSSW base directory/your working directory?

if [ $1 -eq 0 ]; then
    source <any sh file>
fi