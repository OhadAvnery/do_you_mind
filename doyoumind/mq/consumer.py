import pika
import click
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot
from ..constants import SUPPORTED_FIELDS


#from ..cli import CommandLineInterface
#cli = CommandLineInterface()

@click.group()
def main():
    pass
def callback_from_parser(parser):
    def callback_func(channel, method, propreties, body):
        return parser(context_from_snapshot(body), body)
    return callback_func

@main.command()
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5672, type=int)
def consume(host, port):
    #port = int(port) #in case we sent a string
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=SERVER_EXCHANGE, exchange_type='fanout')

    for parser in __parsers__:
        for field in parser.fields:
                if field not in SUPPORTED_FIELDS:
                    continue
        parser_name = parser.__name__
        print(f"consumer- parser: {parser_name}")
        channel.queue_declare(queue=parser_name, durable=True)
        channel.queue_bind(exchange=SERVER_EXCHANGE, queue=parser_name)
        channel.basic_consume(queue=parser_name, on_message_callback=callback_from_parser(parser), auto_ack=True)

    channel.start_consuming()
    print("done consuming!")

if __name__ == '__main__':
    print(f"consumer.py yo")
    main()
