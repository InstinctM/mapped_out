#!/bin/bash

#
# Script to start development server
#

#run the following to initialise the database file if it doesnt exist:
#python api/init.py

echo Killing running servers...
killall -w flask
killall -w uvicorn

echo Starting Flask web server...

export PYTHONHASHSEED=0  # make sure hash function returns the same result every time

cd web
export FLASK_APP=web.py
export FLASK_ENV=development  # Comment out for production
flask run --host localhost --port 8080 &


echo Starting FastAPI server...

cd ../api
uvicorn main:app --host localhost --port 8000 --reload &
