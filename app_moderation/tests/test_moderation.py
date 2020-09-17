import pytest
import sys 
import os
sys.path.insert(0, "/home/francois/workspace/10_formation/app_moderation")
from .main import hello_world

def test_hello():
    response = hello_world.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, World!'
