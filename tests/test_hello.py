#!/usr/bin/env python

"""Tests for `seshkit` package."""

from click.testing import CliRunner
import pytest
import re

from seshkit import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.top)
    assert result.exit_code == 0
    assert "Usage: sesh" in result.output

    help_result = runner.invoke(cli.top, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help +Show this message and exit", help_result.output)


def test_command_version():
    result = CliRunner().invoke(cli.top, ["--version"])
    assert re.match(r"\d+\.\d+\.\d+", result.output)
