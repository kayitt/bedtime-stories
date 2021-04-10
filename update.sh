#!/bin/bash

set -e

echo 'Go to the project'

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

echo 'Upgrade pip'

/usr/local/bin/python3.9 -m pip install --upgrade pip

echo 'Install dependencies'

$HOME/.local/bin/pip install -r etl/requirements.txt

echo 'Run ETL...'

/usr/local/bin/python3.9 etl/src/main.py

echo 'Run ETL... DONE!'
