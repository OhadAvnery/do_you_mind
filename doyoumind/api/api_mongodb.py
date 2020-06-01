from furl import furl
import json
import pymongo


class APIMongoDB:
    '''
    An implementation of the API server with mongodb.
    (For full documentation of the methods, see the api.api module)
    '''
    def __init__(self, db_url):
        self.url = furl(db_url)
        self.client = pymongo.MongoClient(host=self.url.host, port=self.url.port)
        self.db = self.client.db


    def get_users(self):
        '''
        returns a list of all users.
        Each entry contains the user id and username.
        '''
        users_list = list(self.db.users.find())
        result = []
        for user_data in users_list:
            user = {'user_id': user_data['user_id'], 'username': user_data['username']}
            result.append(user)
        return json.dumps(result)

    def get_user(self, user_id):
        '''
        returns a users' details (not including the snapshots)s.
        '''
        user = self.db.users.find_one({'user_id': user_id})
        if not user:
            return None
        user = user.copy()
        del user['snapshots'], user['_id']
        return json.dumps(user)

    def get_snapshots(self, user_id):
        '''
        return the users' snapshots (only their timestamps).
        '''
        user = self.db.users.find_one({'user_id': user_id})
        if not user:
            return None
        return json.dumps(user['snapshots'])

    def get_snapshot(self, user_id, timestamp):
        '''
        return the given topics for a snapshot.
        The snapshot is given by the id of its user, and by its timestamp.
        NOTE: the timestamp is given by a float. (num. of seconds since ...)
        '''
        snap = self.db.snapshots.find_one({'user_id': user_id, 'datetime': timestamp})
        if not snap:
            return None

        non_topic_fields = ['user_id', 'datetime', '_id']
        available_topics = [field for field in snap if field not in non_topic_fields]
        return json.dumps(available_topics)


    def get_result(self, user_id, timestamp, result_name):
        snap = self.db.snapshots.find_one({'user_id': user_id, 'datetime': timestamp})
        if not snap:
            return None
        return json.dumps(snap[result_name])
