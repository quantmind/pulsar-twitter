Pulsar Twitter
=====================

Pulsar queue plugin to stream tweets from Twitter


Accounts
------------

This application can be configured to hoock into multiple accounts:

.. code:: javascript

    [
        {
            "access_token": "Access token",
            "access_token_secret": "Access token secret",
            "stream_filter": {
                "track": "python,javascript",
                "follow": "quantmind,lsbardel"
            }
        },
        ...
    ]
