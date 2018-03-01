import logging
import json
import os

from flask import Flask, request


__version__ = "0.1.6"
__all__ = ['GitWebhook']


class BitbucketParser:

    def parse(self, request):

        data = json.loads(request.data.decode())

        repository = str(data['repository']['full_name'])
        event = str(request.headers['X_EVENT_KEY']).replace("repo:", "")

        branches = []
        if event in data:
            for change in data[event]['changes']:
                if change['new']['type'] == 'branch':
                    branches.append(change['new']['name'])
                if change['old']['type'] == 'branch':
                    branches.append(change['old']['name'])

        return repository, event, list(set(branches)), data


class GitWebhook:

    def __init__(self, host, port=80, uri="/", **kwargs):

        self._host = str(host)
        self._port = int(port)
        self._uri = str(uri)
        self._kwargs = kwargs

        self.event = {}
        self._handlers = {}

        self._parsers = {
            "bitbucket": BitbucketParser()
        }

        self._app = Flask(__name__)
        self._app.secret_key = os.urandom(32)
        self._app.add_url_rule(self._uri, None, self._handle_request, methods=['GET', 'POST'])

    def get_app(self):
        return self._app

    def event(self, repository=None, types=None):
        def decorator(f):
            try:
                for e in types:
                    self.add_handler(f, repository, e)
            except TypeError:
                self.add_handler(f, repository)
            return f
        return decorator

    def run(self):
        self._app.run(host=self._host, port=self._port, **self._kwargs)

    def add_handler(self, f, repository=None, type=None):
        if repository is None:
            repository = "*"
        if type is None:
            type = "*"
        if repository not in self._handlers:
            self._handlers[repository] = {}
        self._handlers[repository][type] = f

    def _get_parser(self, request):
        try:
            useragent = request.headers['User-Agent'].lower()
            if "bitbucket" in useragent:
                return self._parsers['bitbucket']
        except KeyError:
            pass
        return None

    def _handle_request(self):
        try:

            self.event = None

            parser = self._get_parser(request)
            if parser is None:
                return ""

            event = parser.parse(request)

            if event is None:
                return ""

            repository, type, branches, raw_data = event
            req_repository = repository
            req_type = type

            if repository not in self._handlers:
                req_repository = repository
                repository = "*"
                if repository not in self._handlers:
                    return ""

            if type not in self._handlers[repository]:
                req_type = type
                type = "*"
                if type not in self._handlers[repository]:
                    return ""

            self.event = {
                "type": req_type,
                "repository": req_repository,
                "affected_branches": branches,
                "raw_data": raw_data
            }

            self._handlers[repository][type]()
        except:
            logging.exception("Uncaught exception when request handling")
        return ""
