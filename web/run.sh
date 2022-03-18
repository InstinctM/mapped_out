#!/bin/bash

export FLASK_APP=web.py
export FLASK_ENV=development  # Comment out for production
flask run --port 8080
