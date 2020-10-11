import boto3
from pathlib import Path as StdPath

from seshkit.stubs import SeshProfile


class S3Client:
    def __init__(self, profile: SeshProfile, bucket=None):
        self._client = boto3.client("s3", **profile.creds)

    def download(self, bucket, key):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
        """
        resp = self.client.head_object(Bucket=bucket, Key=key)
        return resp

    def head(self, bucket, key):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object

         TODO:
            - works on live server
            - test
            - handle exceptions

        """
        resp = self.client.head_object(Bucket=bucket, Key=key)
        return resp

    def upload_file(self, filename, bucket, key=None, acl="private") -> dict:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

        TODO:
            - works on live server
            - test
            - handle upload_file exceptions
        """
        extra_args = {}
        extra_args["ACL"] = acl

        filepath = StdPath(filename)
        if key is None:
            key = filepath.name

        upload_response = self.client.upload_file(
            Filename=filename, Bucket=bucket, Key=key, ExtraArgs=extra_args
        )
        # at this point, upload has finished
        return self.head(bucket, key)

    @property
    def client(self):
        return self._client
