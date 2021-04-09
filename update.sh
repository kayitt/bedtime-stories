#!/bin/bash

set -e

echo 'Run ETL...'

python3.9 etl/src/main.py

echo 'Run ETL... DONE!'
