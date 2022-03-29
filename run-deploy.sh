#!/bin/bash

#
# Script to start development server
#

#run the following to initialise the database file if it doesnt exist:
#python api/init.py

export PYTHONHASHSEED=0 & 
cd web
export FLASK_APP=web.py
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 8080 &

cd ../api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
