""" Name:           __iniy__.py
    Created:        2015/02/18
    Author:         Mike Ghen <mikeghen@brandeis.edu>
    Purpose:        This is a small flask application which is powered by mod_wsgi
                    and serves as a UI for authorizing via OAuth with the FITBIT
                    API.
    Changelog:      2015/02/19 - Initial creation
"""
from flask import Flask
import logging
from logging import Formatter
from logging import FileHandler
import fitbit.api
import fitbit

LOG_FILE = '/var/log/groupfit.log'
APP_DEBUG = True

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'GROUPFIT!'
    

if __name__ == '__main__':
    """ Set up file debugging"""
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    """ Set add both handlers"""
    app.logger.addHandler(file_handler)
    app.debug = APP_DEBUG
    app.run()

