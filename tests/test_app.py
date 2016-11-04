import unittest
import asyncio

from pulsar import send


class TestTwitter(unittest.TestCase):
    apps = ()

    @classmethod
    async def setUpClass(cls):
        from example.manage import app
        app = app()
        cls.apps = await app.start()
        cls.api = await app.api().start()

    @classmethod
    def tearDownClass(cls):
        coros = [send('arbiter', 'kill_actor', c.name) for c in cls.apps]
        return asyncio.gather(*coros)

    def test_twitter_consumer(self):
        api = self.api
        self.assertEqual(len(api.consumers), 2)
        self.assertEqual(api.consumers[1], api.twitter)
