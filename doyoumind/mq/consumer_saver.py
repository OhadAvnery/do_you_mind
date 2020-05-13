from furl import furl
import pika
from .constants import SAVER_EXCHANGE
from ..parsers.constants import __parsers__
#from ..utils.context import context_from_snapshot

def make_callback(callback, topic):
    def actual_callback(channel, method, properties, body):
        callback(topic)(body)
    return actual_callback



def make_rabbitmq_consumer_saver(f, callback):
    print("consumer_saver.py: setting up a consumer")
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    exchange = SAVER_EXCHANGE     
    channel.exchange_declare(exchange=exchange, exchange_type='direct')


    for parser in __parsers__:
        #the callback should take 4 parameters instead of 1- here we fix it 
        parser_name = parser.__name__ 
        topic = parser_name[6:] #parse_feelings --> feelings
        actual_callback = make_callback(callback, topic)
        queue_name = f"{exchange}/{parser_name}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, routing_key=parser_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
        print(f"CONSUMER_SAVER: consuming the queue {queue_name}, topic: {topic}.")

    return lambda : channel.start_consuming()

class ConsumerSaver:
    def __init__(self, url, callback):
        """
        callback- a function that takes a parser as input, and returns a callback function.
        (this callback function works on ONE parameter- the msg.)
        """
        print("creating ConsumerSaver object")
        f = furl(url)
        self.url = f
        self.consume = CONSUMER_SAVER_SETUPS[f.scheme](f, callback)
        print("created ConsumerSaver object")
       


CONSUMER_SAVER_SETUPS = {'rabbitmq': make_rabbitmq_consumer_saver}

'''
@main.command('consume')
#@click.option('--host', '-h', default='127.0.0.1', type=str)
#@click.option('--port', '-p', default=5672, type=int)
@click.argument('consume_url', type=str)
@click.argument('publish_url', type=str)
def consume_cli(consume_url, publish_url):

    publisher = Publisher(publish_url, SERVER_EXCHANGE)
    publish = publisher.publish
    consumer = Consumer(consume_url, publish, SERVER_EXCHANGE)
    consumer.consume()'''


if __name__ == '__main__':
    print(f"consumer_saver.py yo")

