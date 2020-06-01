[![Build Status](https://travis-ci.com/OhadAvnery/do_you_mind.svg?branch=master)](https://travis-ci.com/OhadAvnery/do_you_mind)
[![Documentation Status](https://readthedocs.org/projects/do-you-mind/badge/?version=latest)](https://do-you-mind.readthedocs.io/en/latest/?badge=latest)
[![CodeCov](https://i.imgur.com/l7YTBgz.png)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)


# doyoumind

The project is responsible for uploading user snapshots, parsing them and visualising the results.
(that is, assuming you already have a brain-reading device. This one's on you; we're developers, not engineers.) 
For full documentation, [click here.](https://do-you-mind.readthedocs.io/en/latest)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/OhadAvnery/do_you_mind.git
    ...
    $ cd do_you_mind
    ```

2. Run the installation script and activate the virtual environment (also building the docker image):

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [doyoumind] $ # oooweeee!
    ```

3. There aren't really any tests, but if you'd like to see a green dot, run:

    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `doyoumind` package provides the following subpackages:

- `client`

    This package allows the user to stream cognition snapshots to a server.
    It provides the 'upload_sample' method, whose parameters are:
    -host, port: the server's host and port (usually '127.0.0.1',8000 respectively).
    -path: the snapshots sample file. (Either uncompressed, or compressed with .gz)
    -read_type: the type of the sample.
    this parameter is optional, and defaults to 'protobuf' (so the samples it takes have the form described in readers/doyoumind.proto). 
    protobuf is also the only format that works for now- there's also a 'binary' format, but it hasn't been fully fleshed out.

    API example-
    ```pycon
    >>> from doyoumind.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```
    CLI example-
    ```sh
    $ python -m doyoumind.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
    ```


- `server`

    This package runs a server at a given host+port, listening to multiple clients, receiving snapshots from them and sending them to various publishers.
    It provides the 'run_server' method, whose parameters are:
    -host, port: the host and port to run from (usually '127.0.0.1',8000 respectively).
    -database: the drive url for the project's database, where the server will send information about new users to. Defaults to 'mongodb://127.0.0.1:27017'. (currently only supports mongodb)
    -publish: a function that's activated on any received snapshot.
    could also be a drive URL for a message queue, for which the server publishes all snapshots.
    (currently only supports rabbitmq)
    -data: the data directory to save the snapshot's data blob's to, defaults to ./snaps.

    API example-
    ```python
    >>> from doyoumind.server import run_server
    >>> def print_message(message):
    ...     print(message)
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    … # listen on host:port and pass received messages to publish
    ```
    CLI example-
    ```sh
    $ python -m doyoumind.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
    ```
- `parsers`

    This package includes parser functions- mini-services that, given a snapshot's raw data, produce a parsed result of it. Each parser produces a different topic (pose, feelings, depth image and color image). For full information about each parser, read their documentation.
    **run_parser-** an API function. Accepts a parser name and some raw data, as consumed from the message queue, and returns the result, as published to the message queue. 
    example-
    ```python
    >>> from doyoumind.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
    ```
    **parse-** a CLI function. Accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as published to the message queue (optionally redirecting it to a file).
    example-
    ```sh
    $ python -m doyoumind.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
    ```
    **run-parser-** a CLI function. Runs the topic's parser as a service, which works with a message queue indefinitely.
    example-
    ```sh
    $ python -m doyoumind.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
    ```
    **run-all-parsers-** a new CLI function. Runs as a service *all* available parsers (given that the server supports all their required fields), working with a message queue indefinitely.
    example-
    ```sh
    $ python -m doyoumind.parsers run-all-parsers 'rabbitmq://127.0.0.1:5672/'
    ```
    _**Q: I want to add a new parser. What should I do?**_
    Glad you asked!
    If you want to parse a new topic, X:
    -In the 'parsers' package, add a new file called X.py.
    -In it, add a function called parse_X. This function should take as input a Context object (representing a directory) and snapshot data, and return the parsed data. 
    The result is a json dictionary, with the keys:
    'parser': the name of the parsed topic (X).
    '[X]': the actual result of the parse, to be saved in the database.
    'user_id': the user's id.
    -parse_X.fields should be all the snapshot fields required for parsing X.
    When running the pipeline, the new parser will be dynamically added to the program and be parsed in its own topic in the mq.
    In order to make the parse result appear in the GUI, you should also add a new 'render_X' function in the render_topic.js script.

- `saver`

    A package that contains a Saver object.
    The saver connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the database.
    API example:
    ```python
    >>> from doyoumind.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```
    **save-** the CLI version: accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database (given by a driver url at the flag -d, defaults to 'mongodb://127.0.0.1:27017').
    Example:
    ```sh
    python -m doyoumind.saver save                     \
      -d/--database 'mongodb://127.0.0.1:27017' \
     'pose'                                       \
     'pose.result' 
    ```
    **run-saver-** a CLI function. Runs the saver as a service, which works with a message queue indefinitely. The saver then subscribes to all relevant topics its capable of consuming, and saves to the database.
    Example:
    ```sh
    $ python -m doyoumind.saver run-saver  \
      'mongodb://127.0.0.1:27017' \
      'rabbitmq://127.0.0.1:5672/'
    ```

- `API`

    Allows the user to send GET requests through various API endpoints, getting information from the database.
    You can build the API server using an API function:
    ```python
    >>> from doyoumind.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'mongodb://127.0.0.1:27017',
    ... )
    … # listen on host:port and serve data from database_url
    ```
    Or using a CLI function:
    ```sh
    $ python -m doyoumind.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'mongodb://127.0.0.1:27017'
     ```
     For full information about the API endpoints, see the documentation on api/api.py.
- `CLI`

    consumes the API and reflects it. 
    Examples:
    ```sh
    $ python -m doyoumind.cli get-users
    …
    $ python -m doyoumind.cli get-user 42
    …
    $ python -m doyoumind.cli get-snapshots 42
    …
    $ python -m doyoumind.cli get-snapshot 42 1575446887.412
    …
    $ python -m doyoumind.cli get-result 42 1575446887.412 'pose'
    …
     $ python -m doyoumind.cli get-result 42 1575446887.412 'pose' -s 'foo.json'
    #using the -s flag in get-result means that instead of printing the result, it saves the data to the given file path
    ```
    
- `GUI`

    Consumes the API and reflects it, using React.
    Has various pages showing the list of users, for each user its list of snapshots, and for each snapshot its various parser results in  (hopefully) decent visualisations.
    It provides the following API:
    ```python
    >>> from doyoumind.gui import run_server
    >>> run_server(
    ...     host = '127.0.0.1',
    ...     port = 8080,
    ...     api_host = '127.0.0.1',
    ...     api_port = 5000,
    ... )
    ```
    And the following CLI:
    ```sh
    $ python -m doyoumind.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
    ```
    in all four fields, the values shown are the default values given in the CLI.

## Deployment

    Finally, all server-side processes (server+message queue+parsers+database+API+GUI) are neatly packed in a docker container. 
    The docker build has been executed inside the install.sh script. If you wish to run the container, you may do it using:
    ```sh 
    ./scripts/run_pipeline.sh
    ```
    and then use the client, API, CLI and GUI as you normally do, each connecting to its default host+port.
    *Warning:* if you wish to run the docker, you should first verify that no other processes run on the same host+port pairs (that means you can't run a local rabbitmq process on port 5672, etc).
    To stop the run, simply execute:
    ```sh 
    ./scripts/stop_pipeline.sh
    ```