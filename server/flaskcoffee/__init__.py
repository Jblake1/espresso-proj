from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import warnings

warnings.simplefilter("ignore")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

from flaskcoffee import routes