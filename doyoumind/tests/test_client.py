import pytest
from doyoumind.client import upload_sample

import requests

@pytest.fixture
def sample():
    return 5

def test_sample(sample):
    assert sample==5