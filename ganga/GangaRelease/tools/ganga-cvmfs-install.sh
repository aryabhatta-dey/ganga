#!/bin/bash

cvmfs_server transaction ganga.cern.ch

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/sft.cern.ch/lcg/releases/LCG_100/Python/3.8.6/x86_64-centos7-gcc9-opt/lib

cd /cvmfs/ganga.cern.ch/Ganga/install

/cvmfs/sft.cern.ch/lcg/releases/LCG_100/Python/3.8.6/x86_64-centos7-gcc9-opt/bin/python3 -m venv $1

. $1/bin/activate

pip install --upgrade pip setuptools

pip install git+https://github.com/ganga-devs/ganga.git@$1#egg=ganga[LHCb] 

sed -i '/from __future__ import print_function/a \
import os, sys \
sys.path.append('/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib/python3.8/site-packages')\
if not 'LD_LIBRARY_PATH' in os.environ.keys():\
    os.environ['LD_LIBRARY_PATH'] = '/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib64:/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib64'\
    os.execv(sys.argv[0], sys.argv)\
elif not '/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib64:/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib64' in os.environ['LD_LIBRARY_PATH']:\
    os.environ['LD_LIBRARY_PATH'] += ':/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib64:/cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc9-opt/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib:/cvmfs/sft.cern.ch/lcg/releases/gcc/9.2.0-afc57/x86_64-centos7/lib64'\
    os.execv(sys.argv[0], sys.argv)' $1/bin/ganga

deactivate

rm -f /cvmfs/ganga.cern.ch/Ganga/install/LATEST

ln -s /cvmfs/ganga.cern.ch/Ganga/install/$1 /cvmfs/ganga.cern.ch/Ganga/install/LATEST

cd ~

cvmfs_server publish ganga.cern.ch


