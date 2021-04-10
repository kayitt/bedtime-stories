#!/bin/bash

set -e

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

echo 'Upgrade pip'

python3.9 -m pip install --upgrade pip

echo 'Install dependencies'

pip install -r etl/requirements.txt

echo 'Run ETL...'

python3.9 etl/src/main.py

echo 'Run ETL... DONE!'
