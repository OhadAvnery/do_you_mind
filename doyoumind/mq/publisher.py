from furl import furl
import pika

#from parsers.main_parser import MainParser, Context
from ..constants import SUPPORTED_FIELDS
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from ..parsers.constants import __parsers__



class Publisher:
    def __init__(self, url):
        f = furl(url)
        self.url = f
        self.publish = PUBLISHER_SETUPS[f.scheme](f)


def make_rabbitmq_publisher(f):
    host, port = f.host, f.port
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=SERVER_EXCHANGE, exchange_type='fanout')
    for parser in __parsers__:
        parser_name = parser.__name__
        channel.queue_declare(queue=parser_name, durable=True)
        channel.queue_bind(exchange=SERVER_EXCHANGE, queue=parser_name)
    def publish(msg):
        channel.basic_publish(exchange=SERVER_EXCHANGE, routing_key='', body=msg)
        print("published message!")
    return publish


'''def publish_by_url(url, msg):
    """url: a url of the form 'rabbitmq://127.0.0.1:5672/' """
    print(f"publish_by_url - url: {url}")
    f = furl(url)
    print(f"publish_by_url - f: {f}")
    print(f"publish_by_url - scheme: {f.scheme}")
    publisher_func = PUBLISHERS[f.scheme]
    print(f"scheme: {f.scheme}, publisher func: {publisher_func}")
    publisher_func(url, msg)
    #main_parser = MainParser(SUPPORTED_FIELDS)
    #main_parser.parse(context, msg)

def publish_rabbit_mq(url, msg):
    f = furl(url)
    
    #channel.queue_declare(queue=QUEUE_NAME)'''
    


PUBLISHER_SETUPS = {'rabbitmq': make_rabbitmq_publisher}

