import json
from flask import url_for

KNOWN_REPO = "user/repo"
KNOWN_TYPE = "push"

UNKNOWN_REPO = "unknown/unknown"
UNKNOWN_TYPE = "unknown"


def build_event(event_type, repository, branch, data):
    return {
        "type": event_type,
        "repository": repository,
        "affected_branches": [branch],
        "raw_data": data
    }


def check_bitbucket_webhook(gwh, client, event_type, repository, branch, hit_expected=False):

    data = '{"%s": {"changes": [{"old": {"type": "branch", "name": "%s"}, "new": {"type": "branch", ' \
           '"name": "%s"}}]},"repository": {"full_name": "%s"}}' % (event_type, branch, branch, repository)

    client.post(url_for('_handle_request'),
                headers={"X_EVENT_KEY": "repo:{}".format(event_type), "User-Agent": "Bitbucket-Webhooks/2.0"},
                data=data.encode())
    if hit_expected:
        assert gwh.event == build_event(event_type, repository, branch, json.loads(data))
    else:
        assert gwh.event is None
