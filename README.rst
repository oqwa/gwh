GitWebHook
==========

This is a simple tool that will help you handle Git webhooks. Now it supports the following services:

* Bitbucket


Installation
------------

.. code-block:: text

    pip install gwh


Usage cases
-----------

If you want to handle any event from any repository:

.. code-block:: python

    from gwh import GitWebhook

    gwh = GitWebhook()

    @gwh.handle()
    def event():
        print(gwh.event['repository'])
        print(gwh.event['type'])
        print(gwh.event['affected_branches'])
        print(gwh.event['raw_data'])

If you want to handle push from specific repository:

.. code-block:: python

    @gwh.handle(repository="user/repo", types=['push'])
    def event():
        if "dev" in gwh.event['affected_branches']:
            print("pushed")

Finally, you need to pass request from your webserver to GitWebhook handler. It will be Flask in this example:

.. code-block:: python

    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/")
    def webhook():
        gwh.handle_request(request.headers, request.data)

Feedback
--------

Bug reports, feature requests, pull requests, any feedback, etc. are welcome.
