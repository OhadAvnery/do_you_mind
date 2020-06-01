from furl import furl
import pika
from .constants import SAVER_EXCHANGE
from ..parsers.constants import __parsers__


def __make_callback(callback, topic):
    '''
    Helper function. 
    Given a semi-callback function of the form callback: topic --> (body --> result),
    and the given topic parsed,
    returns a valid callback function of the form callback: channel, method, properties, body --> result.

    :param callback: a function that takes a topic as input, and returns a callback function.
    :type callback: function str-->(str-->?)
    :param topic: the topic that was parsed
    :type topic: str
    :return: a valid callback using the topic
    :rtype: function (str, str, str, str) --> ?
    '''
    def actual_callback(channel, method, properties, body):
        callback(topic)(body)
    return actual_callback


def rabbitmq_consumer(f, callback):
    """
    Given a driver url for the saver's rabbitmq message queue, 
    and a callback function of the form topic --> (body --> result),
    create a consumer function that connects indefinitely to the mq, applying the given callback
    on every consumed message.

    :param f: the driver's url
    :type f: furl.furl
    :param callback: a function that takes a topic as input, and returns a callback function.
    :type callback: function str-->(str-->?)
    :returns: the consume function
    :rtype: function none-->none
    """

    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    exchange = SAVER_EXCHANGE     
    channel.exchange_declare(exchange=exchange, exchange_type='direct')

    for parser in __parsers__:
        # the callback should take 4 parameters instead of 1- here we fix it 
        parser_name = parser.__name__ 
        topic = parser_name[6:]  # parse_feelings --> feelings
        actual_callback = __make_callback(callback, topic)
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
        
    return lambda: channel.start_consuming()


class ConsumerSaver:
    def __init__(self, url, callback):
        """
        Creates a new ConsumerSaver object, that consumes data from the saver's mq
        (connecting to the mq according to the driver url, and applying the given callback
        on every consumed message on all topics).

        :param url: the mq driver's url
        (currently only supports the format 'rabbitmq://id:port/')
        :type url: str
        :param callback: a function that takes a topic as input, and returns a callback function.
        :type callback: function str-->(str-->?)
        :return: the ConsumerSaver object
        :rtype: ConsumerSaver
        """
        f = furl(url)
        self.url = f
        self.consume = DRIVERS[f.scheme](f, callback)

       
DRIVERS = {'rabbitmq': rabbitmq_consumer}
