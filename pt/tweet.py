import json
from asyncio import Queue

from pq import api

from pulsar import ensure_future
from pulsar.apps.http import OAuth1


class Tweet(api.Message):

    def __init__(self, *args, **kw):
        self.__dict__.update(*args, **kw)


class Account:
    interval1 = 0
    interval2 = 0
    interval3 = 0
    public_stream = 'https://stream.twitter.com/1.1/statuses/filter.json'

    def __init__(self, consumer, api_key, api_secret, account):
        secret = account.get("access_token_secret")
        self.processed = 0
        self.consumer = consumer
        self.logger = consumer.logger
        self.token = account.get("access_token")
        self.filter = account.get("stream_filter")
        self.oauth = OAuth1(api_key,
                            client_secret=api_secret,
                            resource_owner_key=self.token,
                            resource_owner_secret=secret)
        self._queue = Queue(loop=self._loop)
        self._buffer = []
        self._worker = ensure_future(self._queue_worker(), loop=self._loop)

    @property
    def _loop(self):
        return self.consumer._loop

    def connect(self):
        '''Connect to twitter streaming endpoint.
        If the connection is dropped, the :meth:`reconnect` method is invoked
        according to twitter streaming connection policy_.
        '''
        ensure_future(self.consumer.http.post(
            self.public_stream,
            data=self.filter,
            pre_request=self.oauth,
            on_headers=self._connected,
            data_processed=self._process_data,
            post_request=self._reconnect
        ), loop=self._loop)

    def close(self):
        if self._worker:
            worker = self._worker
            self._worker = None
            worker.cancel()
            return worker

    def info(self):
        return {
            "processed": self.processed
        }

    # HOOKS

    def _connected(self, response, **kw):
        '''Callback when a succesful connection is made.
        Reset reconnection intervals to 0
        '''
        if response.status_code == 200:
            self.logger.info(
                'Successfully connected with twitter streaming')
            self.interval1 = 0
            self.interval2 = 0
            self.interval3 = 0

    def _process_data(self, response, **kw):
        '''Callback passed to :class:`HttpClient` for processing
        streaming data.
        '''
        if self.consumer.closing():
            response.transport.close()
            return
        if response.status_code == 200:
            data = response.recv_body()
            while data:
                idx = data.find(b'\r\n')
                if idx < 0:  # incomplete data - add to buffer
                    self._buffer.append(data)
                    data = None
                else:
                    self._buffer.append(data[:idx])
                    data = data[idx + 2:]
                    msg = b''.join(self._buffer)
                    self._buffer = []
                    if msg:
                        body = json.loads(msg.decode('utf-8'))
                        if 'disconnect' in body:
                            msg = body['disconnect']
                            self.logger.warning('Disconnecting (%d): %s',
                                                msg['code'], msg['reason'])
                        elif 'warning' in body:
                            message = body['warning']['message']
                            self.logger.warning(message)
                        else:
                            self._queue.put_nowait(Tweet(body))

    def _reconnect(self, response, exc=None):
        '''Handle reconnection according to twitter streaming policy_
        .. _policy: https://dev.twitter.com/docs/streaming-apis/connecting
        '''
        if self.consumer.closing():
            return
        loop = self._loop
        if response.status_code == 200:
            gap = 0
        elif not response.status_code:
            # This is a network error, back off lineraly 250ms up to 16s
            self.interval1 = gap = min(self.interval1 + 0.25, 16)
        elif response.status_code == 420:
            gap = 60 if not self.interval2 else max(2 * self.interval2)
            self.interval2 = gap
        else:
            if response.status_code >= 400:
                self.logger.error(
                    'Could not connect to twitter streaming API,'
                    ' status code %s' % response.status_code)
            gap = 5 if not self.interval3 else max(2 * self.interval3, 320)
            self.interval3 = gap

        loop.call_later(gap, self.connect)

    async def _queue_worker(self):
        while not self.consumer.closing():
            tweet = await self._queue.get()
            tweet.token = self.token
            try:
                await self.consumer.pubsub.publish('new', tweet)
            except Exception:
                self.logger.exception(
                    'Critical exception while publishing tweet',
                    exec_info=True
                )
            self.processed += 1
            if not self.processed % 10:
                self.logger.info('Account "%s" processed %d tweets',
                                 self.token, self.processed)
        self._worker = None
