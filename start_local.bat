@echo off
set DB_CONNECTION=sqlite:///data.db
python ./app.py
REM python ./reset_database.py