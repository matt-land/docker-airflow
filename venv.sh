#!/usr/bin/env bash
# this is for running airflow dags locally
# run this script and tell pycharm to use the copy of python in /venv/bin/python2.7
set -e

# remove old venv
if [ -d "venv" ]; then
    rm -rf venv
fi


# first install libs into ./src
#pip2 install -r live_requirements.txt --no-cache-dir

virtualenv venv --no-site-packages --python=python3

#clone the requirements file from
source venv/bin/activate && pip2 install -r requirements.txt -r

echo ""
echo "Run the following to start virtual env:"
echo ""
echo "source venv/bin/activate"
echo ""

