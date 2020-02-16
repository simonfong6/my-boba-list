"""
Does an example s3-upload to a bucket.
Assumes that there exists the following AWS config files in ~/.aws/ :
~/.aws/credentials
```
[default]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY

```

~/.aws/config
```
[default]
region=us-west-2

```

Additonally if you want your bucket files to be read from public, you need to
set your bucket policy with this:
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-boba-list/*"
        }
    ]
}
```
"""
import os

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

filename = 'samoyed.jpeg'
# Read binary file.
data = open(filename, 'rb')
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
print(f"You should be able to access this file at https://{bucket_name}.s3-us-west-2.amazonaws.com/{key}")
