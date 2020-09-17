import pytest
import sys 
import os
from main import app
from queries.moderation import moderation_api
import config

def test_hello():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_moderation():
    # Get comment from the POST body
    comment = 'Ceci est une phrase de test.'
    result_moderation = moderation_api(comment)
    assert isinstance(result_moderation, dict) == True

def test_listmoderation():

    # Get comment from the POST body
    comment = 'Ceci est une phrase de test.'
    comment_list = list(comment.split(" ")) 
    comment_list = [x.lower() for x in comment_list]
    assert isinstance(comment_list, list) == True

    # Recup forbidden words
    f = open("app_moderation/checklist.txt", "r")
    forbidden_list = f.read()
    forbidden_list = list(forbidden_list.split("\n"))
    forbidden_list = [x.lower() for x in forbidden_list]
    assert isinstance(forbidden_list, list) == True


