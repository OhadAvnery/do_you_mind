from furl import furl
import pika
from .constants import SERVER_EXCHANGE

class ConsumerParserAtomic:
    def __init__(self, url, topic, callback):
        f = furl(url)
        self.url = f
        self.consume = CONSUMER_PARSER_ATOMIC_SETUPS[f.scheme](f, topic, callback)

def make_callback(callback):
    def actual_callback(channel, method, properties, body):
        callback(body)
    return actual_callback

def make_rabbitmq_consumer_parser_atomic(f, topic, callback):
    '''
    Topic- the name of the parser we want to publish to.
    Callback- the function that works on its data.
    '''
    params = pika.ConnectionParameters(host=f.host, port=f.port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    exchange = SERVER_EXCHANGE
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    
    actual_callback = make_callback(callback)
    parser_name = f"parse_{topic}"
    queue_name = f"{exchange}/{parser_name}"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=actual_callback, auto_ack=True)
    print(f"CONSUMER_PARSER_ATOMIC: consuming the queue {queue_name}.")
    
    return lambda : channel.start_consuming()


CONSUMER_PARSER_ATOMIC_SETUPS = {'rabbitmq': make_rabbitmq_consumer_parser_atomic}