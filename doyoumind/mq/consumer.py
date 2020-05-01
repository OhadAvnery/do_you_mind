import pika
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from constants import SUPPORTED_FIELDS
from parsers.constants import __parsers__

params = pika.ConnectionParameters(localhost)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange=SERVER_EXCHANGE, exchange_type='fanout')

for parser_name in SUPPORTED_FIELDS:
    channel.queue_declare(queue=parser_name)
    channel.queue_bind(exchange=SERVER_EXCHANGE, queue=parser_name)
    callback_func = lambda channgel, method, properties, body: 
