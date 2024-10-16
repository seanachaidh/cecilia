#!/bin/bash

python3 manage.py migrate
python3 manage.py createtestuser
# moet dit opsplitsen omdat dit enkel in debug modus moet gebeuren
python3 -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
