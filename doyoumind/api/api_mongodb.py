from furl import furl
import json
import pymongo

class APIMongoDB:
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
        print(f"api_mongodb/get_users: users list- {users_list}")
        result = []
        for user_data in users_list:
            #user_json = json.loads(user_data)
            user = {'user_id': user_data['user_id'], 'username': user_data['username']}
            result.append(user)
        print(f"api_mongodb/get_users: {result}")
        return json.dumps(result)

    def get_user(self, user_id):
        '''
        returns a users' details (not including the snapshots)s.
        '''
        user = self.db.users.find_one({'user_id':user_id})
        '''if not user:
            print("api_mongodb/get_user: get rekt buddy")
            return 404, 'user not found'
        '''
        if not user:
            return None
        user = user.copy()
        del user['snapshots'], user['_id']
        #print(f"api_mongodb - get_user- our result: {user}")
        return json.dumps(user)

    def get_snapshots(self, user_id):
        '''
        return the users' snapshots (only their timestamps).
        '''
        user = self.db.users.find_one({'user_id':user_id})
        print(f"api_mongodb/get_snapshots: {user}")
        if not user:
            return None
            #return 404, 'user not found'
        return json.dumps(user['snapshots'])

    def get_snapshot(self, user_id, timestamp):
        '''
        return the given topics for a snapshot.
        The snapshot is given by the id of its user, and by its timestamp.
        NOTE: the timestamp is given by a float. (num. of seconds since ...)
        '''
        snap = self.db.snapshots.find_one({'user_id':user_id,'datetime':timestamp})
        if not snap:
            return None

        print(f"api_mongodb/get_snapshot: {snap}")
        non_topic_fields = ['user_id', 'datetime', '_id']
        available_topics = [field for field in snap if field not in non_topic_fields]
        return json.dumps(available_topics)


    def get_result(self, user_id, timestamp, result_name):
        snap = self.db.snapshots.find_one({'user_id':user_id,'datetime':timestamp})
        if not snap:
            return None
        print(f"api_mongodb/get_result: {json.dumps(snap[result_name])}")
        return json.dumps(snap[result_name])

    """
    def get_result_data(self, user_id, timestamp, result_name):
        '''
        NOTE: here we can assume that result_name is a topic having data.
        '''
        snap = self.db.snapshots.find_one({'user_id':user_id,'datetime':timestamp})
        if not snap:
            return None
        path = snap[result_name]
        return send_file(path, mimetype='image/jpg')
        #return result
    """