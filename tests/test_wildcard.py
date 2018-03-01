import pytest

from gwh import *
from tests.utils import *


@pytest.fixture
def app():
    app = GitWebhook()
    app.add_handler(lambda: None)
    return app


def test_bitbucket(app):
    check_bitbucket_webhook(app, KNOWN_TYPE,   KNOWN_REPO,   "master", hit_expected=True)
    check_bitbucket_webhook(app, UNKNOWN_TYPE, KNOWN_REPO,   "master", hit_expected=True)
    check_bitbucket_webhook(app, KNOWN_TYPE,   UNKNOWN_REPO, "master", hit_expected=True)
    check_bitbucket_webhook(app, UNKNOWN_TYPE, UNKNOWN_REPO, "master", hit_expected=True)
