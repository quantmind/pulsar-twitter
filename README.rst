:Badges: |license|  |pyversions| |status| |pypiversion|
:Master CI: |master-build| |coverage-master|
:Downloads: http://pypi.python.org/pypi/pulsar-twitter
:Source: https://github.com/quantmind/pulsar-twitter
:Mailing list: `google user group`_
:Design by: `Quantmind`_ and `Luca Sbardella`_
:Platforms: Linux, OSX, Windows. Python 3.5 and above
:Keywords: server, asynchronous, concurrency, actor, process, queue, tasks, redis


.. |pypiversion| image:: https://badge.fury.io/py/pulsar-twitter.svg
  :target: https://pypi.python.org/pypi/pulsar-twitter
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/pulsar-twitter.svg
  :target: https://pypi.python.org/pypi/pulsar-twitter
.. |license| image:: https://img.shields.io/pypi/l/pulsar-twitter.svg
  :target: https://pypi.python.org/pypi/pulsar-twitter
.. |status| image:: https://img.shields.io/pypi/status/pulsar-twitter.svg
  :target: https://pypi.python.org/pypi/pulsar-twitter
.. |downloads| image:: https://img.shields.io/pypi/dd/pulsar-twitter.svg
  :target: https://pypi.python.org/pypi/pulsar-twitter
.. |master-build| image:: https://img.shields.io/travis/quantmind/pulsar-twitter/master.svg
  :target: https://travis-ci.org/quantmind/pulsar-twitter
.. |coverage-master| image:: https://coveralls.io/repos/github/quantmind/pulsar-twitter/badge.svg?branch=master
  :target: https://coveralls.io/github/quantmind/pulsar-twitter?branch=master

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
