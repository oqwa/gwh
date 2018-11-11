from gwh import *
from tests.utils import *

app = GitWebhook()
app.add_handler(lambda: None, repository=KNOWN_REPO, type=KNOWN_TYPE)


def test_bitbucket():
    check_bitbucket_webhook(app, KNOWN_TYPE,   KNOWN_REPO,   "master", hit_expected=True)
    check_bitbucket_webhook(app, UNKNOWN_TYPE, KNOWN_REPO,   "master", hit_expected=False)
    check_bitbucket_webhook(app, KNOWN_TYPE,   UNKNOWN_REPO, "master", hit_expected=False)
    check_bitbucket_webhook(app, UNKNOWN_TYPE, UNKNOWN_REPO, "master", hit_expected=False)


def test_gitlab():
    check_gitlab_webhook(app, KNOWN_TYPE,   KNOWN_REPO,   "master", hit_expected=True)
    check_gitlab_webhook(app, UNKNOWN_TYPE, KNOWN_REPO,   "master", hit_expected=False)
    check_gitlab_webhook(app, KNOWN_TYPE,   UNKNOWN_REPO, "master", hit_expected=False)
    check_gitlab_webhook(app, UNKNOWN_TYPE, UNKNOWN_REPO, "master", hit_expected=False)
