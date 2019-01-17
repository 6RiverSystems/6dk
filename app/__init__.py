import bunyan
import logging
import sys
import json

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_material import Material
from flask_mail import Mail
from flask_moment import Moment

from config import Config
from app.plugins.loaders.rule_loader import Rule
from app.plugins.loaders.profile_loader import DkProfile
from app.plugins.loaders.user_loader import DkUser


app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
material = Material(app)
mail = Mail(app)
moment = Moment(app)

login.login_view = 'login'
logger = logging.getLogger()
logHandler = logging.StreamHandler(stream=sys.stdout)
formatter = bunyan.BunyanFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)

logger.info('loading message rules')
with open('app/templates/json/rules.json', 'r') as f:
	rule = Rule(json.loads(f.read()), app.config)


logger.info('loading standard dk user')
with open('app/templates/json/standard_user.json', 'r') as f:
	standard_user = json.loads(f.read())
	dk_user = DkUser(standard_user)

logger.info('loading standard dk profile')
with open('app/templates/json/standard_profile.json', 'r') as f:
	standard_profile = json.loads(f.read())

with open('app/templates/json/profile_name_A.txt', 'r') as f:
	adjectives = f.read().splitlines()

with open('app/templates/json/profile_name_B.txt', 'r') as f:
	nouns = f.read().splitlines()

dk_profile = DkProfile(standard_profile, adjectives, nouns)


from app import models
from app.api import admin_routes, fs_routes, wms_routes
from app.ui import (account_routes, application_routes, auth_routes, docs_routes,
					errors_routes, explorer_routes, feed_routes, profile_routes,
					faq_routes)