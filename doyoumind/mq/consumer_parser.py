import click
from furl import furl
import pika
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from .publisher_saver import PublisherSaver
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot
from ..constants import SUPPORTED_FIELDS

def make_callback(callback, parser):
    def actual_callback(channel, method, properties, body):
        callback(parser)(body)
    return actual_callback

@click.group()
def main():
    pass

def make_rabbitmq_consumer_parser(f, callback):
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    exchange = SERVER_EXCHANGE
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    for parser in __parsers__:
        #the callback should take 4 parameters instead of 1- here we fix it 
        actual_callback = make_callback(callback, parser)
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
        print(f"CONSUMER_PARSER: consuming the queue {queue_name}.")
    
    return lambda : channel.start_consuming()
    

class ConsumerParser:
    def __init__(self, url, callback):
        """
        callback- a function that takes a parser as input, and returns a callback function.
        (this callback function works on ONE parameter- the msg.)
        exchange- the name of the exchange we're working with.
        """
        f = furl(url)
        self.url = f
        self.consume = CONSUMER_PARSER_SETUPS[f.scheme](f, callback)




CONSUMER_PARSER_SETUPS = {'rabbitmq': make_rabbitmq_consumer_parser}

@main.command('consume-from-server')
@click.argument('consume_url', type=str)
@click.argument('publish_url', type=str)
def consume_from_server_cli(consume_url, publish_url):
    """consume_url- a string of the form 'rabbitmq://host:port/' 
    (to consume the snapshots from)
    publish_url- a string of the form 'rabbitmq://host:port/' 
    (to publish the result of the parsers to)
    """
    publisher = PublisherSaver(publish_url)
    publish = publisher.publish #takes parser as parameter and returns another function
    consumer = ConsumerParser(consume_url, publish)
    consumer.consume()



if __name__ == '__main__':
    print(f"consumer_parser.py yo")
    main()
