#!/usr/bin/env python3
"""
Backend for mybobalist.
"""
import logging

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import render_template
from flask import url_for

# Configure logging.
logging.basicConfig(filename='logs/server.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)


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


def main(args):

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