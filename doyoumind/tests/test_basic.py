import pytest
from doyoumind.client import upload_sample
from ..server import run_server

def test_example():
    '''
    This is a dumb test example, 
    just to give travisCI something to execute,
    as well as a 'sanity check' that all imports are OK.
    '''
    assert 6==6