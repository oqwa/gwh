GitWebHook
==========

This is a simple Flask tool that will help you handle Git webhooks. Now it supports the following services:

* Bitbucket


Installation
------------

.. code-block:: text

    pip install gwh


Basic usage
-----------

.. code-block:: python

    import gwh

    app = GitWebhook(host="127.0.0.1", port=8080)

    @app.event(repository="oqwa/gwh", types=['push'])
    def event():
        print(app.event['repository'])
        print(app.event['type'])
        print(app.event['affected_branches'])
        print(app.event['raw_data'])

    app.run()

Feedback
--------

Bug reports, feature requests, pull requests, any feedback, etc. are welcome.