#!/bin/bash

set -e

# echo 'Upgrade pip'

# python3.9 -m pip install --upgrade pip

# echo 'Install dependencies'

# SCRIPT=`realpath $0`
# SCRIPTPATH=`dirname $SCRIPT`

# pip install -r $SCRIPTPATH/etl/requirements.txt

echo 'Run ETL...'

python3.9 etl/src/main.py

echo 'Run ETL... DONE!'