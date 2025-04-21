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
import logging
import sys 

warnings.simplefilter("ignore")

basedir = os.path.abspath(os.path.dirname(__file__))

# Correctly calculate the path to the SvelteKit client build output
# frontend_build_path = os.path.join(os.path.dirname(basedir), 'build') # Old incorrect path
svelte_client_build_path = os.path.abspath(os.path.join(os.path.dirname(basedir), '.svelte-kit', 'output', 'client'))

logging.basicConfig(level=logging.DEBUG,
                    stream=sys.stderr,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s')
logging.getLogger().debug("STANDARD_LOGGER: Basic config applied.")

# Check if the calculated path actually exists before passing it to Flask
# static_dir = None # No longer needed with direct Flask config
# if os.path.exists(frontend_build_path):
#     static_dir = frontend_build_path
# else:
#     # Log a warning if the build path doesn't exist during startup
#     print(f"Warning: Frontend build directory not found at {frontend_build_path}")

# Configure Flask to serve static files directly from the SvelteKit build output
app = Flask(__name__,
            static_folder=svelte_client_build_path,  # Serve files from here
            static_url_path='',          # Make files accessible from the root URL (e.g., /images/...)
            template_folder=svelte_client_build_path) # Also look for templates (like index.html) here

# print(f"DEBUG_INIT: Flask app.static_folder = {app.static_folder}", file=sys.stderr) # Keep for debugging if needed
# sys.stderr.flush()

# --- Add these lines ---
if not app.debug: # Only configure logging if Flask debug mode is off
    app.logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.logger.info('Flask logger level set to DEBUG') # Confirm logger setup
# --- End of added lines ---

# Add this log line right after app initialization to check the static path
# app.logger.info(f"Flask static_folder configured to: {app.static_folder}") # Logged automatically by Flask now

# Store the build path in app.config - useful for the catch-all route if needed
if os.path.exists(svelte_client_build_path):
    app.config['FRONTEND_BUILD_PATH'] = svelte_client_build_path
    # logging.getLogger().debug(f"STANDARD_INIT: Frontend build dir FOUND at {svelte_client_build_path}")
else:
    app.config['FRONTEND_BUILD_PATH'] = None
    # logging.getLogger().warning(f"STANDARD_INIT: Frontend build dir NOT FOUND at {svelte_client_build_path}")

# logging.getLogger().info(f"STANDARD_INIT: Using build path: {app.config.get('FRONTEND_BUILD_PATH')}")
# if app.config.get('FRONTEND_BUILD_PATH') is None:
#      logging.getLogger().error("STANDARD_INIT: FRONTEND_BUILD_PATH is None! Frontend serving will likely fail.")

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
# --- Log URL Map AFTER routes are defined/imported ---
log = logging.getLogger(__name__)
# Add a check to ensure routes were imported before logging map
try:
    log.info(f"STANDARD_INIT: Flask URL Map:\n{app.url_map}")
except Exception as e:
    log.error(f"STANDARD_INIT: Error logging URL map - routes likely not imported yet? {e}")
# ---