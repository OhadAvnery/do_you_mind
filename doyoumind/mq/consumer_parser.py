import click
from furl import furl
import pika
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from .publisher_saver import PublisherSaver
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot
from ..constants import SUPPORTED_FIELDS

def __make_callback(callback, parser):
    '''
    Helper function. 
    Given a semi-callback function of the form callback: parser --> (body --> result),
    and the given parser function,
    returns a valid callback function of the form callback: channel, method, properties, body --> result.

    :param callback: a function that takes a parser as input, and returns a callback function.
    :type callback: function (str-->str)-->(str-->?)
    :param parser: the parsing function
    :type parser: function str-->str
    :return: a valid callback using the parser
    :rtype: function (str, str, str, str) --> ?
    '''
    def actual_callback(channel, method, properties, body):
        callback(parser)(body)
    return actual_callback

@click.group()
def main():
    pass

def rabbitmq_consumer(f, callback):
    """
    Given a driver url for the server's rabbitmq message queue, 
    and a callback function of the form parser --> (body --> result),
    create a consumer function that connects indefinitely to the mq, applying the given callback
    on every consumed message.

    :param f: the driver's url
    :type f: furl.furl
    :param callback: a function that takes a parser as input, and returns a callback function.
    :type callback: function (str-->str)-->(str-->?)
    :returns: the consume function
    :rtype: function none-->none
    """
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    exchange = SERVER_EXCHANGE
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    for parser in __parsers__:
        #the callback should take 4 parameters instead of 1- here we fix it 
        actual_callback = __make_callback(callback, parser)
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
        Creates a new ConsumerParser object, that consumes data from the server's mq
        (connecting to the mq according to the driver url, and applying the given callback
        on every consumed message on all topics).

        :param url: the mq driver's url
        (currently only supports the format 'rabbitmq://id:port/')
        :type url: str
        :param callback: a function that takes a parser as input, and returns a callback function.
        :type callback: function (str-->str)-->(str-->?)
        :return: the ConsumerParser object
        :rtype: ConsumerParser
        """
        f = furl(url)
        self.url = f
        self.consume = DRIVERS[f.scheme](f, callback)




DRIVERS = {'rabbitmq': rabbitmq_consumer}

@main.command('consume-from-server')
@click.argument('consume_url', type=str)
@click.argument('publish_url', type=str)
def consume_from_server_cli(consume_url, publish_url):
    """
    Connects to the server's queue, and indefinitely consumes snapshots from it,
    parsing them and publishing them to the saver's queue.
    (currently only supports the format 'rabbitmq://id:port/' as url)

    :param consume_url: the server queue's url
    :type consume_url: str
    :param publish_url: the saver queue's url
    :type publish_url: str
    """
    publisher = PublisherSaver(publish_url)
    publish = publisher.publish #takes parser as parameter and returns another function
    consumer = ConsumerParser(consume_url, publish)
    consumer.consume()



if __name__ == '__main__':
    #print(f"consumer_parser.py yo")
    main()
