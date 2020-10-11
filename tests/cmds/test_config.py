#!/usr/bin/env python
from pathlib import Path

import pytest
from click.testing import CliRunner

from seshkit.cmds.config import command as cmd


@pytest.fixture
def sample_config():
    return (
"""
[default]
service = aws
service_creds_path = sample/.aws/credentials
service_profile = seshkituser
output_bucket = my-seshkit-output-bucket
""")

def test_config_help():
    result = CliRunner().invoke(cmd, ['--help'])
    assert 'View and/or edit your seshkit configuration profiles and settings' in result.output

def test_config_prints_existing_config(sample_config):
    """
    if [config_path] exists, and `--profile` isn't set, then it just prints
    contents of [config_path]
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('testconfig.ini', 'w') as f:
            f.write(sample_config)

        result = runner.invoke(cmd, ['--config-path', 'testconfig.ini'])
        assert result.exit_code == 0

        output = result.output.splitlines()
        assert 'Contents of testconfig.ini:' == output[0]
        assert '[default]' == output[1]
        assert 'service = aws' in output

@pytest.mark.skip(reason='Todo')
def test_config_interaction_when_profile_set():
    pass

@pytest.mark.skip(reason='Todo')
def test_config_interaction_for_nonexistent_config_path():
    pass
