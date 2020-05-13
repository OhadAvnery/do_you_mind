import click
from ..mq.consumer_saver import ConsumerSaver
from .saver import Saver

@click.group()
def main():
    pass

@main.command('save')
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', type=str)
@click.argument('topic', type=str)
@click.argument('path', type=str)
def save_cli(database, topic, path):
    with open(path, 'r') as file:
        data = file.read()
    saver = Saver(database)
    saver.save(topic, data)


@main.command('run-saver')
@click.argument('database', type=str)
@click.argument('mq', type=str)
def run_saver(database, mq):
    #TODO: get data from the message queue
    saver = Saver(database)

    def callback(topic):
        return lambda data: saver.save(topic, data)

    consumer = ConsumerSaver(mq, callback)
    print("saver.py: about to consume")
    consumer.consume()

if __name__ == '__main__':
    main()