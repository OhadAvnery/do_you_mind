import pika
import click
from .constants import SERVER_EXCHANGE, SAVER_EXCHANGE
from .publisher import Publisher
from ..parsers.constants import __parsers__
from ..utils.context import context_from_snapshot
from ..constants import SUPPORTED_FIELDS



@click.group()
def main():
    pass

def callback_from_parser(parser, publish):
    def callback_func(channel, method, properties, body):
        parse_result = parser(context_from_snapshot(body), body)
        print(f"consumser callback: got result for {parser}")
        publish(parse_result)
        print(f"consumser callback: published result of {parser}")
    return callback_func


def consume(host, port, publish):
    """host- an addrses, port- an int, 
    publish- a function that publishes the consumed data.
    """
    #port = int(port) #in case we sent a string
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=SERVER_EXCHANGE, exchange_type='fanout')

    for parser in __parsers__:
        parser_name = parser.__name__
        print(f"consumer- parser: {parser_name}")
        channel.queue_declare(queue=parser_name, durable=True)
        channel.queue_bind(exchange=SERVER_EXCHANGE, queue=parser_name)
        channel.basic_consume(queue=parser_name, on_message_callback=callback_from_parser(parser, publish), auto_ack=True)

    channel.start_consuming()


@main.command('consume')
@click.option('--host', '-h', default='127.0.0.1', type=str)
@click.option('--port', '-p', default=5672, type=int)
@click.argument('url', type=str)
def consume_cli(host, port, url):
    """host- an addrses, port- an int, 
    url- a string of the form 'rabbitmq://host:port/'
    """
    publisher = Publisher(url, SAVER_EXCHANGE)
    publish = publisher.publish
    consume(host, port, publish)


if __name__ == '__main__':
    print(f"consumer.py yo")
    main()
