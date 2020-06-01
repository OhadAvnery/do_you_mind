from furl import furl
import pika

from .constants import SAVER_EXCHANGE
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot


class PublisherSaver:
    '''
    A publisher that, given parse results, 
    that gets snapshot results from the server,
    and publishes it to all queues on the server's exchange so it'll get parsed.
    :param url: the mq driver's url
    (currently only supports the format 'rabbitmq://id:port/')
    :type url: str
    :param publish: the publish function
    :type publish: function str-->?
    '''
    def __init__(self, url):
        f = furl(url)
        self.url = f
        self.publish = DRIVERS[f.scheme](f)


def rabbitmq_publisher(f):
    """
    Creates a new exchange with the given name, and binds it to multiple queues,
    each one representing a different parser.
    Returns a function that given a message, publishes it to the exchange using fanout.
    for the publisher-->consumer interaction: SERVER_EXCHANGE.
    for the consumer-->saver: SAVER_EXCHANGE.
    """

    # routing_key is either a constant- '', or it depends on the parser's name.
    # in the server's exchange, we don't need a routing key, as everything is direct.
    # in the saver's exchange, we update the routing key based on the message.
    exchange = SAVER_EXCHANGE
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    for parser in __parsers__:
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)

    def publish(parser):
        def publish_parser(msg):
            result = parser(context_from_snapshot(msg), msg)
            channel.basic_publish(exchange=exchange, routing_key=parser.__name__, body=result)

        return publish_parser

    return publish


DRIVERS = {'rabbitmq': rabbitmq_publisher}
