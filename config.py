import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_TOKENS = ['09dfe030-e97d-4c59-b440-c936d212e0ab']
    DEV_FS_BASE_URL = 'https://devkit.6river.org'
    MAX_PROFILE_COUNT = 5
    ELEMENTS_PER_PAGE = 100
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'rivs@6river.com'
    MAIL_PASSWORD = '6riverrivs'
    FS_AUTH = 'REVWS0lUOnNyYVdUQWRuaFdFcQ=='


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False