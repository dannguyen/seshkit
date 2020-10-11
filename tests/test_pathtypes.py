from pathlib import Path
from urllib.parse import urlparse

import pytest
from seshkit.types.path import resolve_path, File, S3, Web


def test_resolve_file_path_string():
    src = "~/Downloads/hello/world.mp3"
    p = resolve_path(src)
    assert type(p) is File


def test_resolve_file_path_from_path_object():
    src = Path("~/Downloads/hello/world.mp3")
    p = resolve_path(src)
    assert type(p) is File


def test_resolve_s3_path():
    src = "s3://my.bucket.123/path/to/key.json"
    p = resolve_path(src)
    assert type(p) is S3


def test_resolve_s3_path_from_urlparse():
    src = urlparse("s3://my.bucket.123/hello/world.mp3")
    p = resolve_path(src)
    assert type(p) is S3


def test_resolve_web_path():
    src = "https://example.com/hello/world.mp3"
    p = resolve_path(src)
    assert type(p) is Web


def test_resolve_web_path_from_urlparse():
    src = "https://example.com/hello/world.mp3"
    p = resolve_path(src)
    assert type(p) is Web


####################################
### File
####################################
def test_file_properties():
    src = "~/Downloads/hello/world.mp3"
    p = resolve_path(src)

    assert p.raw == src
    assert p.canonical == str(Path(src).expanduser().resolve())
    assert p.basename == "world.mp3"
    assert p.fileext == "mp3"


@pytest.mark.skip(reason="Need to do temp file system stuff")
def test_file_exists():
    p = resolve_path("this/does/exist.mp3")
    assert p.exists() is True

    q = resolve_path("this/does/not-exist.mp3")
    assert p.exists() is False


####################################
### s3
####################################
def test_s3_properties():
    src = "s3://my.bucket.123/hello/world.mp3"
    p = resolve_path(src)

    assert p.raw == src
    assert p.canonical == src
    assert p.basename == "world.mp3"
    assert p.fileext == "mp3"

    assert p.bucket == "my.bucket.123"
    assert p.key == "hello/world.mp3"


@pytest.mark.skip(reason="Not sure how to handle this")
def test_s3_properties_edgecase():
    src = "s3://my.bucket.123/hello/world.foo#bar.mp3?awsProp=12345"
    p = resolve_path(src)
    assert p.basename == "world.foo#bar.mp3"
    assert p.fileext == "mp3"


@pytest.mark.skip(reason="Need to mock botocore access")
def test_s3_exists():
    p = resolve_path("s3://mybucket/this/exists.mp3")
    assert p.exists() is True

    q = resolve_path("s3://mybucket/this/doesnt/exist.mp3")
    assert p.exists() is False


####################################
### web
####################################
def test_web_properties():
    src = "https://example.com/hello/world.mp3?foo=bar#bookmark"
    p = resolve_path(src)
    assert p.raw == src
    assert p.canonical == src
    assert p.basename == "world.mp3"
    assert p.fileext == "mp3"

    # test that urlunparse removes redundancies
    q = resolve_path("https://example.com/data.json?")
    assert q.raw == "https://example.com/data.json?"
    assert q.canonical == "https://example.com/data.json"
    assert q.basename == "data.json"
    assert q.fileext == "json"


@pytest.mark.skip(reason="Figure it out later")
def test_web_properties_edgecase():
    """https://sethmlarson.dev/blog/2020-04-10/why-urls-are-hard-path-params-urlparse"""
    pass


@pytest.mark.skip(reason="Need to mock http requests")
def test_web_exists():
    p = resolve_path("http://example.com/stuff.mp3")
    assert p.exists() is True

    q = resolve_path("http://example.com/not-here.mp3")
    assert p.exists() is False
