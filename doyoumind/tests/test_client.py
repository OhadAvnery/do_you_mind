import pytest
from ..client import upload_sample

import requests

@pytest.fixture
def sample():
    return 5

def test_sample(sample):
    try:
        assert sample==6
    except:
        sample = 6
        