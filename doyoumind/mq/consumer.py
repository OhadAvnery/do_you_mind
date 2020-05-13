import click
from furl import furl
import pika
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from .publisher import Publisher
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot
from ..constants import SUPPORTED_FIELDS



@click.group()
def main():
    pass

'''
def make_rabbitmq_consumer(f, callback, exchange):
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    #routing_key is either a constant- '', or it depends on the parser's name.
    #in the server's exchange, we don't need a routing key, as everything is direct.
    #in the saver's exchange, we update the routing key based on the message.
    if exchange == SERVER_EXCHANGE:
        exchange_type = 'fanout'
        routing_key = lambda x: ''

    else: #exchange==SAVER_EXCHANGE
        exchange_type = 'direct'
        routing_key = lambda parser_name: parser_name
        
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)



    for parser in __parsers__:
        #the callback should take 4 parameters instead of 1- here we fix it 
        actual_callback = lambda channel, method, properties, body: \
            callback(parser)(body)
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        print(f"consumer- parser: {queue_name}")
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=routing_key(parser_name), queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
        print(f"CONSUMER: consuming the queue {queue_name} on the exchange \
            {exchange}. type: {exchange_type}, routing key: {routing_key(parser_name)}.")

    channel.start_consuming()

class Consumer:
    def __init__(self, url, callback, exchange):
        """
        callback- a function that takes a parser as input, and returns a callback function.
        (this callback function works on ONE parameter- the msg.)
        exchange- the name of the exchange we're working with.
        """
        f = furl(url)
        self.url = f
        self.consume = CONSUMER_SETUPS[f.scheme](f, callback, exchange)


CONSUMER_SETUPS = {'rabbitmq': make_rabbitmq_consumer}
'''

@main.command('consume')
#@click.option('--host', '-h', default='127.0.0.1', type=str)
#@click.option('--port', '-p', default=5672, type=int)
@click.argument('consume_url', type=str)
@click.argument('publish_url', type=str)
def consume_cli(consume_url, publish_url):
    """host- an addrses, port- an int, parameters for connecting with rabbitmq.
    url- a string of the form 'rabbitmq://host:port/' (to publish to)
    """
    publisher = PublisherSaver(publish_url)
    publish = publisher.publish
    consumer = Consumer(consume_url, publish)
    consumer.consume()
    #consume(host, port, publish)


if __name__ == '__main__':
    print(f"consumer.py yo")
    main()
