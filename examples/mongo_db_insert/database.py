#!/usr/bin/env python3
"""
MongoDB Database Access Example

Usage:
    ```
    python3 database.py --credential_path ../../credentials/credentials.json
    ```
"""
import datetime
import json
import logging

from bson import json_util
import pymongo


logger = logging.getLogger(__name__)


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

def test_database_connection(connection_string):
    """Creates a post to a database."""

    client = pymongo.MongoClient(connection_string)
    db = client.test


    post = {
        "author": "Mike",
        "text": "Delete this document. This is a TEST.",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
    }

    posts = db.posts

    post_str = json.dumps(post, indent=4, default=json_util.default)
    logger.error("Saving Post to Collection %s: %s", 'posts', post_str)
    post_id = posts.insert_one(post).inserted_id

    print("Successfully added document to database!")


def main(args):

    connection_string = get_connection_string(args.credential_path)

    test_database_connection(connection_string)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--credential_path',
                        help="Credential path, defaults to `credentials.json`",
                        type=str,
                        required=True)

    args = parser.parse_args()
    main(args)