import datetime
from furl import furl
import json
import pymongo
import threading

from ..mq.consumer_saver import ConsumerSaver

lock = threading.Lock()

class Saver:
    '''
    An object that connects to the database and saves information about users and snapshots.
    :param url: the database's driver url
    :type url: furl.furl
    :param save: the saver's save function (chosen according to the drive scheme)
    :type save: function (str,str)-->none
    '''
    def __init__(self, database_url="mongodb://127.0.0.1:27017"):
        """
        Constructs a new Saver object, given the database driver.
        :param url: database driver url, defaults to "mongodb://127.0.0.1:27017"
        (only supports the mongodb scheme)
        :type url: str
        :returns: Saver object
        :rtype: Saver
        """
        print("saver.py: building a new saver")
        f = furl(database_url)
        self.url = f
        self.save = SAVER_SETUPS[f.scheme](f)


   
def make_mongodb_saver(f):
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
        #print(f"saver- save: {data}")
        #print(f"saver- save: {data[topic]}")
        dt = data['datetime'] #we save it as float, not as datetime
        user_id = data['user_id']

        #find if there's already a snapshot with the given timestamp. If not, create one.
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

        #print(f"saver.py/save: done saving {topic}!")

    return save

SAVER_SETUPS = {'mongodb': make_mongodb_saver}
