import bunyan
import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

logger = logging.getLogger()
logHandler = logging.StreamHandler(stream=sys.stdout)
formatter = bunyan.BunyanFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)

from app import models
from app.api import admin_routes, fs_routes, wms_routes