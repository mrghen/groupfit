""" Name:           __iniy__.py
    Created:        2015/02/18
    Author:         Mike Ghen <mikeghen@brandeis.edu>
    Purpose:        This is a small flask application which is powered by mod_wsgi
                    and serves as a UI for authorizing via OAuth with the FITBIT
                    API.
    Changelog:      2015/02/19 - Initial creation
"""
from flask import Flask, session, redirect, url_for, escape, request, g
import logging
from logging import Formatter
from logging import FileHandler
from fitbit.api import FitbitOauthClient
import os
import pprint
import sys
import fitbit.api
import fitbit
import sqlite3

LOG_FILE = '/var/log/groupfit.log'
DATABASE = '/opt/flask/GroupFit/GroupFit/groupfit.db'
APP_DEBUG = True
CLIENT_KEY = '02dc33abfa9241bf8a993689e8865cc9'
CLIENT_SECRET = 'a3677586a65d489187955237b74c549b'

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def hello_world():
    app.logger.debug("Init FitbitOauthClient")
    client = FitbitOauthClient(CLIENT_KEY, CLIENT_SECRET)
   
    app.logger.debug("Get request token")
    token = client.fetch_request_token()
    app.logger.debug('RESPONSE')
    app.logger.debug(token)
     
    # Save the oauth token for use in callback()
    try:
        session['oauth_token'] = token
    except:
        print "Unexpected error:", sys.exc_info()
        raise

    app.logger.debug('* Authorize the request token in your browser\n')
    return '<center><a href="%s">Authorize GroupFit</a></center>' % client.authorize_token_url()


@app.route('/callback', methods=['GET'])
def callback():
    client = FitbitOauthClient(CLIENT_KEY, CLIENT_SECRET)
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = session['oauth_token']
    token = client.fetch_access_token(oauth_verifier, token=oauth_token)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES ('%s', '%s', '%s')" % (token['encoded_user_id'], token['oauth_token'], token['oauth_token_secret']))
    except:
        print "Unexpected error:", sys.exc_info()
        raise
    conn.commit()
    conn.close() 
    return "Success" 

if __name__ == '__main__':
    """ Set up file debugging"""
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    """ Set add both handlers"""
    app.logger.addHandler(file_handler)
    app.debug = APP_DEBUG
    app.logger.debug('About to call FitBitOauthClient()')
    app.run()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def connect_to_database():
    return sqlite3.connect(DATABASE)
