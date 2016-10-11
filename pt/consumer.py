"""
Consume tweets from Twitter streaming API

https://dev.twitter.com/streaming/reference/post/statuses/filter
"""
import asyncio

from pq import api

from pulsar import ImproperlyConfigured, ensure_future
from pulsar.apps.http import HttpClient

from . import __version__
from .tweet import Account


class Twitter(api.ConsumerAPI):
    version = __version__
    accounts = None
    http = None

    def start(self, worker):
        self.http = HttpClient(loop=self._loop)
        self.accounts = {}
        api_key = self.get_param('twitter_api_key')
        api_secret = self.get_param('twitter_api_secret')
        twitter_accounts = self.get_param('twitter_accounts')
        for account in twitter_accounts:
            account = Account(self, api_key, api_secret, account)
            self.accounts[account.token] = account
            account.connect()

    def tick(self):
        if self.closing():
            if self.accounts:
                accounts = self.accounts
                self.accounts = None
                self.logger.info('Closing twitter accounts')
                ensure_future(close(self, accounts), loop=self._loop)
            else:
                self.do_close()

    def info(self):
        if self.accounts:
            return [a.info() for a in self.accounts.values()]

    def get_param(self, name):
        value = self.cfg.get(name)
        if not value:
            raise ImproperlyConfigured(
                'Please specify the "%s" parameter in your %s file' %
                (name, self.cfg.config))
        return value


async def close(self, accounts):
    closing = []
    for account in accounts.values():
        closing.append(account.close())
    await asyncio.gather(*closing, return_exceptions=True)
    self.do_close()
