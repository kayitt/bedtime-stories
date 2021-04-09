#!/bin/bash

set -e

echo 'Pull' > logs.log

git pull origin main

echo 'Run ETL' >> logs.log

python3.9 etl/src/etl.py
