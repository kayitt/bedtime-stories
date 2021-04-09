#!/bin/bash

set -e


echo 'Refresh repository'

git pull origin main

echo 'Run ETL...'

python3.9 etl/src/main.py

echo 'Finished ETL' >> /tmp/bedtime_logs.log
