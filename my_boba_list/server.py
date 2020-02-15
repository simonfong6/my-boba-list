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

from bson.json_util import dumps
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

    drinks = [boba_dict['mango-matcha']]
    return render_template('boba.html.jinja', drinks=drinks)

def drink_form_to_db_schema(drink_form):
    SCHEMA_KEYS_TO_FORM_KEYS = {
        'name': 'drink-name',
        'size': 'size',
        'ice_level': 'ice-level',
        'sugar_level': 'sugar-level',
        'toppings': 'toppings'
    }

    schema_object = {
        'name': 'Mango Matcha',
        'size': 'Large',
        'ice_level': 70,
        'sugar_level': 50,
        'rating': 97,
        'toppings': ['Boba', 'Egg Pudding'],
        'image': '/static/images/boba/mango-matcha.jpg'
    }

    for schema_key, form_key in SCHEMA_KEYS_TO_FORM_KEYS.items():
        schema_object[schema_key] = drink_form[form_key]

    return schema_object

def get_first_element(drink_form):
    DEARRAY = set(['drink-name', 'size', 'ice-level', 'sugar-level'])
    new_dict = {}

    for key, val in drink_form.items():
        if key in DEARRAY:
            new_dict[key] = val[0]
        else:
            new_dict[key] = val

    return new_dict

@app.route('/drinks/create', methods=['GET', 'POST'])
def create_drink():
    if request.method == 'GET':
        return render_template('create-boba-form.html.jinja')
    elif request.method == 'POST':

        logger.info(json.dumps(dict(request.form), indent=4))

        drink_form = dict(request.form)

        drink_form_dearrayed = get_first_element(drink_form)

        drink = drink_form_to_db_schema(drink_form_dearrayed)

        logger.info(json.dumps(drink, indent=4))

        db = get_db()

        drinks_collection = db['drinks']

        drink_id = drinks_collection.insert_one(drink).inserted_id


        return f"I created a drink with id = {drink_id}!"


@app.route('/drinks/view/<drink_name>')
def view_drinks(drink_name):
    db = get_db()

    drinks_collection = db['drinks']
    if drink_name == 'all':
        all_drinks = []
        for drink in drinks_collection.find(): 
            drink_dict = dict(drink)
            all_drinks.append(drink_dict)
            logging.info(dumps(drink_dict, indent=4))

        return render_template('boba.html.jinja', drinks=all_drinks)

        return dumps(all_drinks, indent=4)


def main(args):

    database_connection_string = get_connection_string(args.credential_path)

    # Load default config and override config from an environment variable
    app.config.update(dict(
        DATABASE_CONNECTION_STRING=database_connection_string,
        DATABASE_NAME="my-boba-list-db"
    ))

    if args.debug:
        logger.setLevel(logging.DEBUG)

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