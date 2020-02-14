#!/usr/bin/env python3
"""
Creates a credentials JSON for MongoDB.

Usage:
    ```
    python3 create_credentials.py \
        --user "admin" \
        --password "apassword" \
        --connection_string "mongodb+srv://{admin}:{password}@stuff.net/test?retryWrites=true&w=majority"
    ```
"""
import json
import logging


DEFAULT_CREDENTIAL_PATH = "credentials.json"


logger = logging.getLogger(__name__)


def save_credential_as_json(
        user,
        password,
        connection_string,
        credential_path=DEFAULT_CREDENTIAL_PATH):
    """
    Example:
        {
            "user": "admin",
            "password": "averystrongpassword",
            "connection_string": "mongodb+srv://{user}:{password}@cluster-gbdcm.mongodb.net/test?retryWrites=true&w=majority
        }
        
    """

    credential_dict = {
        'user': user,
        'password': password,
        'connection_string': connection_string
    }

    with open(credential_path, 'w') as file_ptr:
        credential_str = json.dumps(credential_dict, indent=4)
        logger.error("Saving Credentials: %s", credential_str)


        json.dump(credential_dict, file_ptr, indent=4)
        

def main(args):

    save_credential_as_json(
        user=args.user,
        password=args.password,
        connection_string=args.connection_string,
        credential_path=args.credential_path
    )


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--user',
                        help="Database user.",
                        type=str,
                        required=True)
    parser.add_argument('--password',
                        help="Whether or not to run in debug mode.",
                        type=str,
                        required=True)
    parser.add_argument('--connection_string',
                        help="Whether or not to run in prod mode.",
                        type=str,
                        required=True)
    parser.add_argument('--credential_path',
                        help="Credential path, defaults to `credentials.json`",
                        default=DEFAULT_CREDENTIAL_PATH)

    args = parser.parse_args()
    main(args)