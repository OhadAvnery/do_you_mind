from furl import furl
import pika

from .constants import SERVER_EXCHANGE
from ..parsers.constants import __parsers__


class PublisherParser:
    '''
    A publisher that gets snapshot data from the server,
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
    Given a driver url for the server's rabbitmq message queue,
    Bind the server exchange to multiple queues,
    each one representing a different parser.
    Return a function that given a message, publishes it to the exchange using fanout.
    :param f: the driver's url
    :type f: furl.furl
    :returns: the publish function
    :rtype: function str-->?
    """
    exchange = SERVER_EXCHANGE
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    for parser in __parsers__:
        parser_name = parser.__name__
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_name)

    def publish(msg):
        channel.basic_publish(exchange=exchange, routing_key='', body=msg)

    return publish


DRIVERS = {'rabbitmq': rabbitmq_publisher}
