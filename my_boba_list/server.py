#!/usr/bin/env python3
"""
Backend for mybobalist.
"""
import json
import logging

from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

from pymongo import MongoClient

# Configure logging.
logging.basicConfig(filename='logs/server.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)

def get_connection_string(credential_path):
    """Converts credentials JSON to a connection string."""

    with open(credential_path) as file_ptr:
        credential_dict = json.load(file_ptr)

    connection_string = credential_dict['connection_string']

    full_connection_string = connection_string.format(
        user=credential_dict['user'],
        password=credential_dict['password']
    )

    return full_connection_string


def connect_db():
    """Connects to the signinucsd database on mlab servers."""
    db_connection = MongoClient(app.config['DATABASE_CONNECTION_STRING'])
    return db_connection


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'dbConnection'):
        g.dbConnection = connect_db()
    return g.dbConnection[app.config['DATABASE_NAME']]


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'dbConnection'):
        g.dbConnection.close()


@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/boba/<drink_name>')
def boba(drink_name):
    boba_dict = {
        'mango-matcha': {
            'name': 'Mango Matcha',
            'ice_level': 70,
            'sugar_level': 50,
            'rating': 97,
            'toppings': ['Boba', 'Egg Pudding'],
            'image': '/static/images/boba/mango-matcha.jpg'
        }
    }

    context = boba_dict['mango-matcha']
    return render_template('boba.html.jinja', **context)


@app.route('/drinks/create', methods=['GET', 'POST'])
def create_drink():
    if request.method == 'GET':
        return render_template('create-boba-form.html.jinja')
    elif request.method == 'POST':

        logger.info(request.form)

        drink = {
            'name': 'Mango Matcha',
            'ice_level': 70,
            'sugar_level': 50,
            'rating': 97,
            'toppings': ['Boba', 'Egg Pudding'],
            'image': '/static/images/boba/mango-matcha.jpg'
        }

        db = get_db()

        drinks_collection = db['drinks']

        # drink_id = drinks_collection.insert_one(drink).inserted_id
        drink_id = 'blah'


        return f"I created a drink with id = {drink_id}!"


def main(args):

    database_connection_string = get_connection_string(args.credential_path)

    # Load default config and override config from an environment variable
    app.config.update(dict(
        DATABASE_CONNECTION_STRING=database_connection_string,
        DATABASE_NAME="my-boba-list-db"
    ))

    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=args.port
    )


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p', '--port',
                        help="Port that the server will run on.",
                        type=int,
                        default=3034)
    parser.add_argument('--credential_path',
                        help="Credential path, defaults to `credentials.json`",
                        type=str,
                        required=True)
    parser.add_argument('-d', '--debug',
                        help="Whether or not to run in debug mode.",
                        default=False,
                        action='store_true')
    parser.add_argument('--prod',
                        help="Whether or not to run in prod mode.",
                        default=False,
                        action='store_true')

    parser.add_argument('--no_log',
                        help="Whether to not keep logs.",
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    main(args)