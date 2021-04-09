#!/bin/bash

set -e

git pull origin main

python3.9 etl/src/etl.py
