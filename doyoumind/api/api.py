from furl import furl
#import json
import pymongo

'''class API:
    def __init__(self, db):
        self.db = db'''

db = None

def run_api_server(host='127.0.0.1', port='5000', database_url='mongodb://127.0.0.1:27017'):
    f = furl(database_url)
    client = pymongo.MongoClient(host=f.host, port=f.port)
    db = client.db

def get_users():
    '''
    returns a list of all users.
    Each entry contains the user id and username.
    '''
    users_list = list(db.users.find())
    result = []
    for user_data in result:
        user_json = json.loads()
        user = {'user_id': user_json['user_id'], 'username': user_json['username']}
        result.append(user)
    return json.dumps(result)

def get_user(user_id):
    '''
    returns a users' details (not including the snapshots)s.
    '''
    user = db.users.find_one({'user_id':user_id})
    if not user:
        return None
    user = user.copy()
    del user['snapshots']
    return json.dumps(user)

def get_snapshots(user_id):
    '''
    return the users' snapshots (only their timestamps).
    '''
    user = db.users.find_one({'user_id':user_id})
    if not user:
        return None
    return json.dumps(user.snapshots)

def get_snapshot(user_id, timestamp):
    '''
    return the given topics for a snapshot.
    The snapshot is given by the id of its user, and by its timestamp.
    NOTE: the timestamp is given by a float. (num. of seconds since ...)
    '''
    snap = snapshots.find_one({'user_id':user_id,'datetime':timestamp})
    if not snap:
        return None

    non_topic_fields = ['user_id', 'datetime']
    available_topics = [field for field in snap if field not in non_topic_fields]
    return json.dumps(available_topics)


def get_result(user_id, timestamp, result_name):
    snap = snapshots.find_one({'user_id':user_id,'datetime':timestamp})
    if not snap:
        return None
    return json.dumps(s[result_name])



#TODO: end connection by client.close()