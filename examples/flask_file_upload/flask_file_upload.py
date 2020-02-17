#!/usr/bin/env python3
"""
Python 3.8

Combining Flask and AWS to upload files to S3.
"""
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

import os

import boto3
import uuid

@app.route('/upload')
def upload_file_site():
    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(secure_filename(f.filename))
        import boto3

        # Let's use Amazon S3
        s3 = boto3.resource('s3')
        data = f

        uid = uuid.uuid4()
        filename = f'{uid}.jpeg'
        # Read binary file.
        folder = 'test'
        key = os.path.join(folder, filename)
        bucket_name = 'my-boba-list'

        # Upload file.
        s3.Bucket(bucket_name).put_object(
            Key=key,
            Body=data,
            ContentType='image/jpg'         # Meta data so computers know what this is.
        )

        print(f"Succesfully uploaded file as {key}")
        public_file_url = f"https://{bucket_name}.s3-us-west-2.amazonaws.com/{key}"
        print(f"You should be able to access this file at {public_file_url}")
        return f'file uploaded successfully at <a href="{public_file_url}">{public_file_url}</a>'
		
if __name__ == '__main__':
    port = 3034
    site_url = f'http://localhost:{port}/upload'
    print(f"Site starting at {site_url}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True)