# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    jwt_path = os.path.normpath(os.path.join(basedir, os.pardir))+'/.config.json'
    private_key_path = os.path.normpath(os.path.join(basedir, os.pardir))+'/.private.key'

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')
    FERNET_KEY = os.getenv('FERNET_KEY')

    # UI Elements Demo
    CLIENT_ID = os.getenv('CLIENT_ID', '')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
    REDIRECT_URI = os.getenv('REDIRECT_URI', '')
    DEMO_FOLDER_NAME = os.getenv('DEMO_FOLDER_NAME', 'UI Elements Demo')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    

    # JWT Manual Configuration
    JWT_CLIENT_ID = os.getenv('JWT_CLIENT_ID', '')
    JWT_CLIENT_SECRET = os.getenv('JWT_CLIENT_SECRET', '')
    JWT_PUBLIC_KEY_ID = os.getenv('JWT_PUBLIC_KEY_ID', '')
    JWT_PRIVATE_KEY = os.getenv('JWT_PRIVATE_KEY', '')
    JWT_PASSPHRASE = os.getenv('JWT_PASSPHRASE', '')
    JWT_ENTERPRISE_ID = os.getenv('JWT_ENTERPRISE_ID', '')
    JWT_EXPIRATION_SECONDS = os.getenv('JWT_EXPIRATION_SECONDS', 3600)

    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        os.getenv('DB_PASS'     , 'pass'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'appseed_db')
    ) 

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
