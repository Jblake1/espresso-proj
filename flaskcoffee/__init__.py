from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, timezone
import logging
import sys
from logging.handlers import RotatingFileHandler

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

import warnings
import os

warnings.simplefilter("ignore")

basedir = os.path.abspath(os.path.dirname(__file__))

frontend_build_path = os.path.join(os.path.dirname(basedir), 'build')
static_dir = None
if os.path.exists(frontend_build_path):
    static_dir = frontend_build_path
    print(f"DEBUG: Found frontend build path: {static_dir}") # ADD TEMPORARY PRINT
    logging.info(f"Found frontend build path: {static_dir}") # ADD LOGGING
else:
    print(f"WARNING: Frontend build directory not found at {frontend_build_path}") # ADD TEMPORARY PRINT
    logging.warning(f"Frontend build directory not found at {frontend_build_path}. Static files may not be served correctly.") # ADD LOGGING

# Explicitly log the value being passed to Flask
print(f"DEBUG: Initializing Flask with static_folder='{static_dir}'") # ADD TEMPORARY PRINT
logging.info(f"Initializing Flask with static_folder='{static_dir}'") # ADD LOGGING


app = Flask(__name__, static_folder=static_dir)
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Configure logging
log_file_path = os.path.join(basedir, 'app.log')
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting Flask application...")

database_uri = os.environ.get('DATABASE_URL')

if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

# Use app.instance_path if DATABASE_URL is not set
if not database_uri:
    # This constructs the path like: C:\Users\Josh\projects\espresso-project\instance\coffeedata.db
    instance_db_path = os.path.join(app.instance_path, 'coffeedata.db')

    # Ensure the instance folder exists before setting the URI
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating instance folder {app.instance_path}: {e}")
        # Handle error appropriately, maybe raise it or exit

    database_uri = f"sqlite:///{instance_db_path}"

# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'coffeedata.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended practice
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=4)
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh-token'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
# app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token_cookie'

# Log database URI
if database_uri:
    logging.info(f"Using database URI: {database_uri}")
else:
    logging.warning("No database URI found. Using default SQLite configuration.")

# Log frontend build path
if static_dir:
    logging.info(f"Frontend static directory set to: {static_dir}")
else:
    logging.warning("Frontend static directory not found. Static files may not be served.")

# Log JWT configuration
logging.info(f"JWT access token expiration set to: {app.config['JWT_ACCESS_TOKEN_EXPIRES']}")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

from flaskcoffee import models

from flaskcoffee import routes