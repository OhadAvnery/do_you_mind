import datetime
from furl import furl
import json
import pymongo
import threading

from ..mq.consumer_saver import ConsumerSaver

lock = threading.Lock()

class Saver:
    def __init__(self, database_url="mongodb://127.0.0.1:27017"):
        """
        receives a database url, of the form:
        'mongodb://host:port'.
        """
        f = furl(database_url)
        self.url = f
        self.save = SAVER_SETUPS[f.scheme](f)


   
def make_mongodb_saver(f):
    #host, port = f.host, f.port
    client = pymongo.MongoClient(host=f.host, port=f.port)
    db = client.db
    users = db.users
    snapshots = db.snapshots

    def save_user(user_data):
        user_data = json.loads(user_data) 
        user_id = user_data['user_id']
        #print(f"save user- type of user_id: {type(user_id)}")
        #print(f"save user- the data: {user_data}")
        if users.find_one({'user_id':user_id}):
            return
        user_data['snapshots'] = []
        #age_epoch = user_data['birthday']
        #user_data['birthday'] = datetime.datetime.fromtimestamp(age_epoch)
        #print(f"saver- save_user: {user_data}")
        users.insert_one(user_data)


    def save(topic, data):
        """
        receives a topic name (such as 'pose'), and a data from the corresponding message queue,
        and saves the data in the database.
        If topic=='user': saves a new entry for the user.
        (If there's already a user with the same user id, it doesn't do anything.)
        If topic=='snapshot': saves a new entry for the snapshot, inside the user.
        (If there's already a snapshot for the user with the same timestamp, it doesn't do anything.)
        """
        print(f"saver.py/save: about to save {topic}")
        if topic == 'user':
            save_user(data)
            return

        data = json.loads(data)
        print(f"saver- save: {data}")
        print(f"saver- save: {data[topic]}")
        #dt = datetime.datetime.fromtimestamp(data['datetime'])
        dt = data['datetime']
        user_id = data['user_id']

        #find if there's a snapshot with the given timestamp. If not, create one.
        lock.acquire()
        snap = snapshots.find_one({'user_id':user_id,'datetime':dt})
        if not snap:
            users.update_one({'user_id':user_id}, {'$push':{'snapshots':dt}})
            snapshots.insert_one({'user_id':user_id, 'datetime':dt})
        lock.release()

        #update entry
        added_entry = {topic:data[topic]}
        snapshots.update_one({'user_id':user_id,'datetime':dt},
            {'$set':added_entry})

        print(f"saver.py/save: done saving {topic}!")

    return save

SAVER_SETUPS = {'mongodb': make_mongodb_saver}
