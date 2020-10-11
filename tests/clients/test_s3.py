import pytest
import boto3
import botocore

# https://www.patricksoftwareblog.com/monkeypatching-with-pytest/
# https://adamj.eu/tech/2019/04/22/testing-boto3-with-pytest-fixtures/
# https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html#botocore-stub

@pytest.mark.skip(reason='Todo')
def test_basic(monkeypatch):
    def mock_client():
        # return a boto3.Client that has somehow authenticated
        pass

    monkeypatch.setattr(boto3, 'client', mock_client)
    pass
