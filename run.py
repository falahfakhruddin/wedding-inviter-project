# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config
import logging

import os

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG_STATUS')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    # app.logger.info('DBMS Host     = ' + app_config['MONGODB_HOST'])

if __name__ == "__main__":
    app.run()
