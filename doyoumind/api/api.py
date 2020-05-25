import flask
from flask_cors import CORS
from furl import furl
import threading

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
    returns a list of all users.
    Each entry contains the user id and username.
    '''
    #print(f"thread: {threading.currentThread().name}")
    return API.driver.get_users()

@app.route("/users/<int:user_id>")
def get_user(user_id):
    '''
    returns a users' details (not including the snapshots).
    '''
    return return_if_exists(API.driver.get_user(user_id))
    '''result = API.driver.get_user(user_id)
    if not result:
        flask.abort(404)
    return result'''

@app.route("/users/<int:user_id>/snapshots")
def get_snapshots(user_id):
    '''
    return the users' snapshots (only their timestamps).
    '''
    return return_if_exists(API.driver.get_snapshots(user_id))


@app.route("/users/<int:user_id>/snapshots/<float:timestamp>")
def get_snapshot(user_id, timestamp):
    '''
    return the given topics for a snapshot.
    The snapshot is given by the id of its user, and by its timestamp.
    WARNING: it probably dosen't support snapshots made before 1970
    '''
    return return_if_exists(API.driver.get_snapshot(user_id, timestamp))

@app.route("/users/<int:user_id>/snapshots/<float:timestamp>/<result_name>")
def get_result(user_id, timestamp, result_name):
    '''
    return the result of the snapshot's topic's parse.
    '''
    return return_if_exists(API.driver.get_result(user_id, timestamp, result_name))

@app.route("/users/<int:user_id>/snapshots/<float:timestamp>/<result_name>/data")
def get_result_data(user_id, timestamp, result_name):
    '''
    for large data fields, returns the actual data of the parser.
    Returns a 'bytes' object.
    '''
    if result_name not in LARGE_DATA_FIELDS:
        flask.abort(404)
    return API.driver.get_result_data(user_id, timestamp, result_name)



#TODO: end connection by client.close()