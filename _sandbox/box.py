#!/usr/bin/env python3
from configparser import ConfigParser
from IPython import embed as itrace
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import boto3

from seshkit.utils import *
from seshkit.types.path import *
from seshkit.stubs import *

from seshkit.clients.s3 import S3Client
from seshkit.settings import *

def main():
    print('hello there')

    bucket = 'test-seshkit-input-bucket'
    profile = SeshProfile(DEFAULT_SESHKIT_PROFILE_PATH)
    s3client = S3Client(profile)


    itrace()


# def s3_upload_file(filename, bucket, key=None, acl='private') -> dict:
#     """
#     https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

#     TODO: get s3 file path

#     """
#     extra_args = {}
#     extra_args['ACL'] = acl

#     filepath = Path(filename)
#     if key is None:
#         key = filepath.name

#     client = boto3.client('s3')
#     upload_response = client.upload_file(Filename=filename, Bucket=bucket, Key=key, ExtraArgs=extra_args)

#     head_response = client.head_object(Bucket=bucket, Key=key)
#     return head_response


if __name__ == '__main__':
    main()
