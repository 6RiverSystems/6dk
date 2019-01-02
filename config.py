import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_TOKENS = ['09dfe030-e97d-4c59-b440-c936d212e0ab']
    DEV_FS_BASE_URL = 'https://techops3.6river.org'


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False