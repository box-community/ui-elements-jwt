# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present [Box](https://developer.box.com/)
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_caching import Cache
from apps.config import Config


db = SQLAlchemy()
login_manager = LoginManager()

fl_cache = Cache(config={'CACHE_TYPE': Config.CACHE_TYPE,
                          'CACHE_DIR': Config.CACHE_DIR,
                          'CACHE_DEFAULT_TIMEOUT': int(Config.CACHE_DEFAULT_TIMEOUT)})


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    fl_cache.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
    

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

