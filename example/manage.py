from pq.api import PulsarQueue


def app():
    return PulsarQueue(consumers=['pq.api:Tasks', 'pt.consumer:Twitter'],
                       description='Pulsar queue with twitter streaming')


if __name__ == '__main__':
    app().start()
