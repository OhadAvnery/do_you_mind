from connection import Connection
from listener import Listener

with Listener(port=8000) as listener:
    connection = listener.accept()
    print(connection.receive_message()) # prints 'Hello, world!'
