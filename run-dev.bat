!/bin/bash

::
:: Script to start development server
::

echo Killing running servers...
taskkill /IM /F "flask.exe"
taskkill /IM /F "uvicorn.exe"

echo Starting Flask web server...

cd web
set FLASK_APP=web.py
set FLASK_ENV=development  # Comment out for production
flask run --host localhost --port 8080 &


echo Starting FastAPI server...

cd ../api
uvicorn main:app --host localhost --port 8000 --reload &
