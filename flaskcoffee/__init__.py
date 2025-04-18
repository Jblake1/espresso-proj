from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta, timezone

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

# Check if the calculated path actually exists before passing it to Flask
static_dir = None
if os.path.exists(frontend_build_path):
    static_dir = frontend_build_path
else:
    # Log a warning if the build path doesn't exist during startup
    print(f"Warning: Frontend build directory not found at {frontend_build_path}")

app = Flask(__name__, static_folder=static_dir, static_url_path='')
CORS(app, supports_credentials=True)  # Enable CORS for all routes

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

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

from flaskcoffee import models

from flaskcoffee import routes