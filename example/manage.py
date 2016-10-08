from pq.api import TaskApp


def app():
    return TaskApp(consumers=['pq.api:Tasks', 'pt.consumer:Twitter'],
                   description='Pulsar queue with twitter streaming')


if __name__ == '__main__':
    app().start()
