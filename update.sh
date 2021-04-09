#!/bin/bash

set -e

echo 'Pull' >> /tmp/bedtime_logs.log

git pull origin main

echo 'Run ETL' >> /tmp/bedtime_logs.log

python3.9 etl/src/main.py

echo 'Finished ETL' >> /tmp/bedtime_logs.log