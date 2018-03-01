import logging
import json


__version__ = "0.1.8"
__all__ = ['GitWebhook']


class BitbucketParser:

    def __init__(self):
        pass

    def parse(self, headers, body):

        """
        Method extract payload from request data to further working
        :param headers: Dictionary of headers
        :param body: Bytes of request body
        :return: Dictionary with payload
        """

        data = json.loads(body.decode())

        repository = str(data['repository']['full_name'])
        event = str(headers['X_EVENT_KEY']).replace("repo:", "")

        branches = []
        if event in data:
            for change in data[event]['changes']:
                if change['new']['type'] == 'branch':
                    branches.append(change['new']['name'])
                if change['old']['type'] == 'branch':
                    branches.append(change['old']['name'])

        return repository, event, list(set(branches)), data


class GitWebhook:

    def __init__(self):

        self.event = None

        self._handlers = {}
        self._parsers = {
            "bitbucket": BitbucketParser()
        }

    def event(self, repository=None, types=None):

        """
        Decorator to define event handler
        :param repository: Events from only this repository will be handled. If None - any repositories will be handled
        :param types: Only this type of event will be handler. If None - any types will be handled
        :return:
        """

        def decorator(f):
            try:
                for e in types:
                    self.add_handler(f, repository, e)
            except TypeError:
                self.add_handler(f, repository)
            return f
        return decorator

    def add_handler(self, f, repository=None, type=None):

        """
        Add event handler
        :param f: Handling function
        :param repository: Events from only this repository will be handled. If None - any repositories will be handled
        :param type: Only this type of event will be handler. If None - any types will be handled
        :return:
        """

        if repository is None:
            repository = "*"

        if type is None:
            type = "*"

        try:
            self._handlers[repository][type] = f
        except KeyError:
            self._handlers[repository] = {type: f}

    def handle_request(self, headers, body):

        """
        Method passes a request from a web-server to an internal handler. Is implied that:
            * At first, most of git services send their webhook requests as a POST requests
            * Secondly, developer convert a request from his web server to this method on his own
        :param headers: Dictionary of headers
        :param body: Bytes of request body
        :return: Status of operation. Boolean. Success or not
        """

        assert isinstance(headers, dict)
        assert isinstance(body, bytes)

        try:

            self.event = None

            parser = self._get_parser(headers, body)
            if parser is None:
                return False

            event = parser.parse(headers, body)

            if event is None:
                return False

            repository, type, branches, raw_data = event
            req_repository = repository
            req_type = type

            if repository not in self._handlers:
                req_repository = repository
                repository = "*"
                if repository not in self._handlers:
                    return False

            if type not in self._handlers[repository]:
                req_type = type
                type = "*"
                if type not in self._handlers[repository]:
                    return False

            self.event = {
                "type": req_type,
                "repository": req_repository,
                "affected_branches": branches,
                "raw_data": raw_data
            }

            self._handlers[repository][type]()
            return True
        except:
            logging.exception("Uncaught exception when request handling")

        return ""

    def _get_parser(self, headers, body):

        """
        Trying to define service from request data
        :param headers: Dictionary of headers
        :param body: Bytes of request body
        :return:
        """

        try:
            useragent = headers['User-Agent'].lower()
            if "bitbucket" in useragent:
                return self._parsers['bitbucket']
        except KeyError:
            pass

        return None
