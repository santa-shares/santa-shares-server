@echo off
set DB_CONNECTION=sqlite:///data.db
python ./reset_database.py
python ./app.py