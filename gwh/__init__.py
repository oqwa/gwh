import logging
import json
import os

from flask import Flask, request


__version__ = "0.1.1"
__all__ = ['GitWebhook']


class BitbucketParser:

    def extract_webhook(self, request):
        data = json.loads(request.data.decode())
        return (
            str(data['repository']['full_name']),
            str(request.headers['X_EVENT_KEY']).replace("repo:", ""),
            data
        )

    def get_pushed_branch(self, data):
        if "push" in data:
            for change in data['push']['changes']:
                if change['new']['type'] == 'branch':
                    return change['new']['name']
        return None


class GitWebhook:

    def __init__(self, host, port=80, uri="/"):

        self._host = str(host)
        self._port = int(port)
        self._uri = str(uri)

        self.event_type = None
        self.event_data = None
        self.event_repository = None
        self.pushed_branch = None
        self._handlers = {}

        self._parsers = {
            "bitbucket": BitbucketParser()
        }

        self._app = Flask(__name__)
        self._app.secret_key = os.urandom(32)
        self._app.add_url_rule(self._uri, None, self._handle_request, methods=['GET', 'POST'])

    def event(self, repository=None, types=None, branches=None):
        def decorator(f):
            try:
                for e in types:
                    self.add_handler(repository, e, branches, f)
            except TypeError:
                self.add_handler(repository, "*", branches, f)
            return f
        return decorator

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def add_handler(self, repository, type, branches, f):
        if repository is None:
            repository = "*"
        if repository not in self._handlers:
            self._handlers[repository] = {}
        self._handlers[repository][type] = (f, branches)

    def _get_parse(self, request):
        try:
            useragent = request.headers['User-Agent'].lower()
            if "bitbucket" in useragent:
                return self._parsers['bitbucket']
        except KeyError:
            pass
        return None

    def _handle_request(self):
        try:

            parser = self._get_parse(request)
            if parser is None:
                return ""

            webhook = parser.extract_webhook(request)

            if webhook is None:
                return ""

            repository, type, data = webhook

            self.event_type = type
            self.event_data = data
            self.event_repository = repository

            if repository not in self._handlers:
                repository = "*"
                if repository not in self._handlers:
                    return ""

            if type not in self._handlers[repository]:
                type = "*"
                if type not in self._handlers[repository]:
                    return ""

            self.pushed_branch = parser.get_pushed_branch(data)

            handler, branches = self._handlers[repository][type]

            if type == "push" and branches is not None:
                if self.pushed_branch not in branches:
                    return ""

            handler()
        except:
            logging.exception("Uncaught exception when request handling")
        return ""
