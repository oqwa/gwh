from gwh import *
from flask import url_for, testing
import json
import requests
import pytest
from tests.utils import *

gwh_app = GitWebhook(host=None, port=0)


@pytest.fixture
def app():
    def event():
        pass
    gwh_app.add_handler(event)
    return gwh_app.get_app()


def test_200ok(client):
    assert client.post(url_for('_handle_request')).status_code == 200


def test_bitbucket(client):
    check_bitbucket_webhook(gwh_app, client, KNOWN_TYPE,   KNOWN_REPO,   "master", hit_expected=True)
    check_bitbucket_webhook(gwh_app, client, UNKNOWN_TYPE, KNOWN_REPO,   "master", hit_expected=True)
    check_bitbucket_webhook(gwh_app, client, KNOWN_TYPE,   UNKNOWN_REPO, "master", hit_expected=True)
    check_bitbucket_webhook(gwh_app, client, UNKNOWN_TYPE, UNKNOWN_REPO, "master", hit_expected=True)
