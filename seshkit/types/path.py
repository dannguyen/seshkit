import boto3
import botocore
from pathlib import Path as StdPath
from typing import Union as typeUnion
from urllib.parse import ParseResult as UrlParseResult, urlparse, urlunparse

import requests


class SeshPath(object):
    def __init__(self, path: str):
        if not isinstance(path, str):
            raise TypeError(f"Expected `path` to be str, not {type(path)}")
        self._raw_path_string = path

    def exists(self):
        raise TypeError("Need to implement this in the subclass")

    def __str__(self):
        return self.canonical

    @property
    def basename(self) -> str:
        raise TypeError("Need to implement this in the subclass")

    @property
    def canonical(self) -> str:
        """the cleaned-up normalized str path"""
        raise TypeError("Need to implement this in the subclass")

    @property
    def fileext(self) -> str:
        """simply a string and an implicit guess of filetype"""
        raise TypeError("Need to implement this in the subclass")

    @property
    def raw(self) -> str:
        """the original str object"""
        return self._raw_path_string


class SeshRemotePath(SeshPath):
    def __init__(self, path: str):
        super().__init__(path)
        self._url = urlparse(self._raw_path_string)

    @property
    def basename(self) -> str:
        return StdPath(self._url.path).name

    @property
    def fileext(self) -> str:
        return StdPath(self._url.path).suffix.lstrip(".")


class File(SeshPath):
    def __init__(self, path: str):
        super().__init__(path)
        self._path = StdPath(self._raw_path_string)

    def exists(self):
        return self._path.is_file()

    @property
    def basename(self) -> str:
        return self._path.name

    @property
    def fileext(self) -> str:
        return self._path.suffix.lstrip(".")

    @property
    def canonical(self) -> str:
        return str(self._path.expanduser().resolve())


class S3(SeshRemotePath):
    def __init__(self, path: str):
        super().__init__(path)
        # allow_fragments is False in edge cases where S3 key has a # sign for whatever reason
        self._s3url = urlparse(self._raw_path_string, allow_fragments=False)

    def exists(self):
        """
        https://stackoverflow.com/questions/33842944/check-if-a-key-exists-in-a-bucket-in-s3-using-boto3
        """
        s3 = boto3.resource("s3")
        try:
            obj = s3.Object(self.bucket, self.key).load()
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "404":
                # The object does not exist.
                return False
            else:
                # Something else has gone wrong.
                raise
        else:
            return True

    @property
    def bucket(self) -> str:
        return self._s3url.netloc

    @property
    def canonical(self) -> str:
        return self._raw_path_string

    @property
    def key(self) -> str:
        """TODO: this does not yet handle funky paths, such as pathnames with query strings???"""
        return self._s3url.path.lstrip("/")


class Web(SeshRemotePath):
    def __init__(self, path: str):
        super().__init__(path)

    def exists(self):
        resp = requests.head(self.canonical, allow_redirects=True)
        return resp.status_code == 200

    @property
    def canonical(self) -> str:
        return urlunparse(self._url)


def resolve_path(
    src: typeUnion[str, StdPath, UrlParseResult]
) -> typeUnion[File, S3, Web]:
    if isinstance(src, (StdPath, str)):
        raw_path_string = str(src)
        urlp = urlparse(raw_path_string)
    elif isinstance(src, UrlParseResult):
        raw_path_string = urlunparse(src)
        urlp = src
    else:
        raise TypeError(
            f"`src` is expected to be type str/Path/urllib.parse.ParseResult, not f{type(src)}"
        )

    if urlp.scheme in ("http", "https"):
        return Web(raw_path_string)
    elif urlp.scheme == "s3":
        return S3(raw_path_string)
    else:
        return File(raw_path_string)
