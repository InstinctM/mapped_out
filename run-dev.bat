
::
:: Script to start development server
::
::run the following to initialise the database file (if it doesnt exist):
::python api/init.py
echo Killing running servers...
taskkill /IM /F "uvicorn.exe"

echo Starting Flask web server...

set PYTHONHASHSEED=0

echo Starting FastAPI server...

cd api
start uvicorn main:app --host 0.0.0.0 --port 8000 --reload
