#!/bin/bash

#
# Script to start development server
#

#run the following to initialise the database file if it doesnt exist:
#python api/init.py

echo Killing running servers...
killall -w uvicorn

export PYTHONHASHSEED=0  # make sure hash function returns the same result every time

echo Starting FastAPI server...

cd api
uvicorn main:app --host localhost --port 8000 --reload &
