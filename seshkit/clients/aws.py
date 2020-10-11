import botocore
import boto3
from pathlib import Path as StdPath
from seshkit.stubs import SeshProfile


class AWSClient:
    """just an abstract class for S3 and Transcribe to inherit from"""

    aws_service = "ABSTRACT"  # change in subclass

    def __init__(self, profile: SeshProfile, bucket: str = None):
        self._client = boto3.client(self.aws_service, **profile.creds)

    @property
    def client(self) -> botocore.client.BaseClient:
        return self._client
