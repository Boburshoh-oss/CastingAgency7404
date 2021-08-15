  
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_param = {
    "username": "postgres",
    "password": "admin",
    "db_name": "capstone",
    "dialect": "postgresql"
}
