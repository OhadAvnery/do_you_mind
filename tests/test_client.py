import pytest
from do_you_mind.doyoumind.client import upload_sample

import pytest
import requests

@pytest.fixture
def sample():
    return 5

def test_sample(sample):
    assert sample==5