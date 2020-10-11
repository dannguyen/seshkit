from pathlib import Path

import pytest
from click.testing import CliRunner

from seshkit.stubs import SeshProfile


PROFILEPATH = "seshprofile"
CREDSPATH = "credsfile"

PROFILE_BODY = f"""
[default]
service = aws
service_creds_path = {CREDSPATH}
service_profile = default
output_bucket = my-seshkit-output-bucket

[profiletest]
service = aws
service_creds_path = {CREDSPATH}
service_profile = seshtest
output_bucket = tester-bucket
"""


CREDS_BODY = """
[default]
aws_access_key_id = DEFAULT_ID
aws_secret_access_key = DEFAULT_SECRET

[seshtest]
aws_access_key_id = TEST_ID
aws_secret_access_key = TEST_SECRET
"""


@pytest.fixture
def cdict():
    return {
        "service": "aws",
        "service_creds_path": CREDSPATH,
        "service_profile": "seshkituser",
    }


@pytest.fixture
def t_profilepath(tmpdir):
    p = tmpdir.mkdir("testhometest1").join(PROFILEPATH)
    p = Path(p)
    p.write_text(PROFILE_BODY)
    return str(p)


@pytest.fixture
def t_credspath(tmpdir):
    p = tmpdir.mkdir("testhometest2").join(CREDSPATH)
    p = Path(p)
    p.write_text(CREDS_BODY)
    return str(p)


def test_init_from_dict(cdict):
    """Accepts dict for initialization"""
    p = SeshProfile(cdict)
    for key in SeshProfile.VALID_ATTRIBUTES:
        assert p[key] == getattr(p, key)


@pytest.mark.curious(
    reason="pytest's methods for creating test files/paths is not great"
)
def test_init_from_filepath(t_profilepath):
    """
    pytest's tempfile methods is not good; maybe just use CliRunner.isolated_filesystem
    """
    p = SeshProfile(t_profilepath)
    assert p.service == "aws"
    assert p.service_profile == "default"
    assert p.service_creds_path == CREDSPATH


def test_open_creds():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(CREDSPATH, "w") as f:
            f.write(CREDS_BODY)

        with open(PROFILEPATH, "w") as f:
            f.write(PROFILE_BODY)

        p = SeshProfile(PROFILEPATH)
        assert p.service_profile == "default"
        assert p.service_creds_path == CREDSPATH

        creds = p.creds
        assert type(creds) is dict
        assert creds["aws_access_key_id"] == "DEFAULT_ID"
        assert creds["aws_secret_access_key"] == "DEFAULT_SECRET"


@pytest.mark.curious(reason="refactor/DRY isolated_filesystem usage")
def test_open_creds():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(CREDSPATH, "w") as f:
            f.write(CREDS_BODY)

        with open(PROFILEPATH, "w") as f:
            f.write(PROFILE_BODY)

        p = SeshProfile(PROFILEPATH, "profiletest")
        assert p.service_profile == "seshtest"

        creds = p.creds
        assert creds["aws_access_key_id"] == "TEST_ID"
        assert creds["aws_secret_access_key"] == "TEST_SECRET"
