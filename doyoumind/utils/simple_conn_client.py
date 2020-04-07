from connection import Connection

with Connection.connect(host='127.0.0.1', port=8000) as connection:
    connection.send_message('Hello, world!') # prepends size
