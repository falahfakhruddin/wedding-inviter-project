# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask, url_for
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path

db = MongoEngine()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home', 'api'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)

    app.logger.info('Service Running With Config Debug is {}!'.format(app.config['DEBUG']))

    if not app.config['DEBUG']:
        #app.logger.info('URI: {}'.format(app.config['MONGODB_HOST']))
        app.config['MONGODB_HOST'] = os.environ.get['MONGODB_HOST']

    register_extensions(app)
    register_blueprints(app)
    return app
