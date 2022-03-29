release: cd api && python init.py
web: export PYTHONHASHSEED=0 && cd api && uvicorn main:app --host 0.0.0.0 --port $PORT --reload
