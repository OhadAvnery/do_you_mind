import flask
from flask_cors import CORS
from furl import furl
import json

from .constants import DRIVERS, LARGE_DATA_FIELDS


class API:
    host = None
    port = None
    driver = None
    def __init__(self, host, port, db_url):
        print("calling API init")
        f = furl(db_url)
        API.host = host
        API.port = port
        API.driver = DRIVERS[f.scheme](db_url)


app = flask.Flask(__name__)
CORS(app)


def run_api_server(host='127.0.0.1', port=5000, database_url='mongodb://127.0.0.1:27017'):
    API(host, port, database_url)
    app.run(host=host, port=port)


def return_if_exists(result):
    if result:
        return result
    flask.abort(404)


@app.route("/users")
def get_users():
    '''
    Returns a list of all users.
    Each entry contains the user id and username.
    :returns: list of users
    :rtype: str
    '''
    return API.driver.get_users()


@app.route("/users/<int:user_id>")
def get_user(user_id):
    '''
    Returns a users' details (not including its snapshots).
    :param user_id: user's id
    :type user_id: int
    :returns: user details
    :rtype: str (json)
    '''
    return return_if_exists(API.driver.get_user(user_id))


@app.route("/users/<int:user_id>/snapshots")
def get_snapshots(user_id):
    '''
    Returns the users' snapshots list (only their timestamps).
    :param user_id: user's id 
    :type user_id: int
    :returns: list of snapshot timestamps
    :rtype: str (json)
    '''
    return return_if_exists(API.driver.get_snapshots(user_id))


@app.route("/users/<int:user_id>/snapshots/<float:timestamp>")
def get_snapshot(user_id, timestamp):
    '''
    Return the given topics for a snapshot.
    The snapshot is given by the id of its user, and by its timestamp.
    WARNING: dosen't support snapshots made before 1970
    :param user_id: user's id 
    :type user_id: int
    :param timestamp: snapshot's timestamp
    :type timestamp: float
    :returns: the snapshot's supported topics
    :rtype: str (json)
    '''
    return return_if_exists(API.driver.get_snapshot(user_id, timestamp))


@app.route("/users/<int:user_id>/snapshots/<float:timestamp>/<result_name>")
def get_result(user_id, timestamp, result_name):
    '''
    Return the result of the snapshot's topic's parse.
    The snapshot is given by the id of its user, and by its timestamp.
    WARNING: dosen't support snapshots made before 1970
    :param user_id: user's id 
    :type user_id: int
    :param timestamp: snapshot's timestamp
    :type timestamp: float
    :param result_name: name of the requested topic
    :type result_name: str
    :returns: the snapshot's supported topics
    :rtype: str (json)
    '''
    return return_if_exists(API.driver.get_result(user_id, timestamp, result_name))


@app.route("/users/<int:user_id>/snapshots/<float:timestamp>/<result_name>/data")
def get_result_data(user_id, timestamp, result_name):
    '''
    For large data fields, returns the actual data of the parser (as a picture).
    Return the result of the snapshot's topic's parse.
    The snapshot is given by the id of its user, and by its timestamp.
    WARNING: dosen't support snapshots made before 1970
    :param user_id: user's id 
    :type user_id: int
    :param timestamp: snapshot's timestamp
    :type timestamp: float
    :param result_name: name of the requested (large-data) topic
    :type result_name: str
    :returns: the result as a file 
    :rtype: file
    '''
    if result_name not in LARGE_DATA_FIELDS:
        flask.abort(404)
    path = json.loads(get_result(user_id, timestamp, result_name))
    return flask.send_file(path)
