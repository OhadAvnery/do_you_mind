from furl import furl
import pika
from .constants import SERVER_EXCHANGE

class ConsumerParserAtomic:
    def __init__(self, url, topic, callback):
        """
        Creates a new ConsumerParserAtomic object, that consumes data from the server's mq
        (connecting to the mq according to the driver url, and applying the given callback
        on every consumed message).
        Unlike the standard consumer, it only consumes ONE topic.

        :param url: the mq driver's url
        (currently only supports the format 'rabbitmq://id:port/')
        :type url: str
        :param callback: a function that takes a parser as input, and returns a callback function.
        :type callback: function (str-->str)-->(str-->?)
        """
        f = furl(url)
        self.url = f
        self.consume = CONSUMER_PARSER_ATOMIC_SETUPS[f.scheme](f, topic, callback)

def __make_callback(callback):
    '''
    Helper function. 
    Given a semi-callback function of the form callback: body --> result,
    and the given parser function,
    returns a valid callback function of the form callback: channel, method, properties, body --> result.

    :param callback: the mq driver's url
    :type callback: str
    :param callback: a function that takes a parser as input, and returns a callback function.
    :type callback: function str-->?
    :return: a valid callback
    :rtype: function (str, str, str, str) --> ?
    '''
    def actual_callback(channel, method, properties, body):
        callback(body)
    return actual_callback

def make_rabbitmq_consumer_parser_atomic(f, topic, callback):
    """
    Given a driver url for the server's rabbitmq message queue, 
    and a callback function of the form parser --> (body --> result),
    create a consumer function that connects indefinitely to the mq, applying the given callback
    on every consumed message.

    :param f: the driver's url
    :type f: furl.furl
    :param topic: name of a topic to be parsed
    :type topic: str
    :param callback: a function that takes a parser as input, and returns a callback function.
    :type callback: function str-->none
    :return: the consume function
    :rtype: function none-->none
    """

    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    exchange = SERVER_EXCHANGE
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    
    actual_callback = __make_callback(callback)
    parser_name = f"parse_{topic}"
    queue_name = f"{exchange}/{parser_name}"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
    print(f"CONSUMER_PARSER_ATOMIC: consuming the queue {queue_name}.")
    
    return lambda : channel.start_consuming()


CONSUMER_PARSER_ATOMIC_SETUPS = {'rabbitmq': make_rabbitmq_consumer_parser_atomic}