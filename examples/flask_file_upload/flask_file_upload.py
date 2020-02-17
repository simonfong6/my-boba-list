#!/usr/bin/env python3
"""
Python 3.8

Combining Flask and AWS to upload files to S3.
"""
import mimetypes
import os
import uuid

import boto3
from flask import Flask, render_template, request
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename


BUCKET_NAME = 'my-boba-list'
DIRECTORY = 'test'
FILE_FORM_NAME = 'file'


app = Flask(__name__)


def generate_unique_filename(filename):
    """Generates a unique filename with the correct extension."""

    uuid_ = uuid.uuid4()

    mime_type, _encoding = mimetypes.guess_type(filename)
    extension = mimetypes.guess_extension(mime_type)
    
    unique_filename = f"{uuid_}{extension}"

    return unique_filename



@app.route('/upload')
def upload_file_site():
    """Serves the upload page."""
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    """Handles the file upload from the form."""
    if request.method == 'POST':
        # Get file from form response.
        file_to_upload = request.files[FILE_FORM_NAME]

        # Generate filename.
        filename_from_user = file_to_upload.filename
        mime_type, _encoding = mimetypes.guess_type(filename_from_user)
        filename = generate_unique_filename(filename_from_user)
        key = os.path.join(DIRECTORY, filename)

        # Upload to S3.
        bucket_name = BUCKET_NAME
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.put_object(
            Key=key,
            Body=file_to_upload,
            ContentType=mime_type         # Meta data so computers know what this is.
        )

        print(f"Succesfully uploaded file as {key}")
        public_file_url = f"https://{bucket_name}.s3-us-west-2.amazonaws.com/{key}"
        print(f"You should be able to access this file at {public_file_url}")
        return f'File uploaded successfully at <a href="{public_file_url}">{public_file_url}</a>'
		
if __name__ == '__main__':
    port = 3034
    site_url = f'http://localhost:{port}/upload'
    print(f"Site starting at {site_url}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True)