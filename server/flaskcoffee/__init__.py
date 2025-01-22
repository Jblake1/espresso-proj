from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import warnings
import os

warnings.simplefilter("ignore")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'coffeedata.db')}"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskcoffee import routes