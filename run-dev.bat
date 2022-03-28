
::
:: Script to start development server
::
::run the following to initialise the database file (if it doesnt exist):
::python api/init.py
echo Killing running servers...
taskkill /IM /F "flask.exe"
taskkill /IM /F "uvicorn.exe"

echo Starting Flask web server...

set PYTHONHASHSEED=0

cd web
set FLASK_APP=web.py
set FLASK_ENV=development  # Comment out for production
start flask run --host localhost --port 8080


echo Starting FastAPI server...

cd ../api
start uvicorn main:app --host localhost --port 8000 --reload
