import bunyan
import logging
import sys
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_material import Material
from flask_moment import Moment

from config import Config
from app.rule_loader import Rule


app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
material = Material(app)
moment = Moment(app)

login.login_view = 'login'
logger = logging.getLogger()
logHandler = logging.StreamHandler(stream=sys.stdout)
formatter = bunyan.BunyanFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)

with open('app/rules.json', 'r') as f:
	logger.info('loading message rules')
	rule = Rule(json.loads(f.read()), app.config)


from app import models
from app.api import admin_routes, fs_routes, wms_routes
from app.ui import routes


