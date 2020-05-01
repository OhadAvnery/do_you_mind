import pika
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot

from ..cli import CommandLineInterface
cli = CommandLineInterface()

@cli.command
def consume(host="127.0.0.1", port=5672):
    port = int(port) #in case we sent a string
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=SERVER_EXCHANGE, exchange_type='fanout')

    for parser in __parsers__:
        parser_name = parser.__name__
        channel.queue_declare(queue=parser_name)
        channel.queue_bind(exchange=SERVER_EXCHANGE, queue=parser_name)
        callback_func = lambda channel, method, properties, body: parser_name(body, context_from_snapshot(body))
        channel.basic_consume(queue=parser_name, on_message_callback=callback_func, auto_ack=True)

    channel.start_consuming()
    print("done consuming!")

if __name__ == '__main__':
    cli.main()