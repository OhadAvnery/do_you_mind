import datetime
from furl import furl
import json
import pymongo

class Saver:
    def __init__(self, database_url="mongodb://127.0.0.1:27017"):
        """
        receives a database url, of the form:
        'mongodb://host:port'.
        """
        f = furl(database_url)
        self.url = f
        self.save = SAVER_SETUPS[f.scheme](f)

@click.group()
def main():
    pass

@main.command('save')
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', type=str)
@click.argument('topic', type=str)
@click.argument('path', type=str)
def save_cli(database, topic, path):
    #TODO: get data from the message queue
    data = "????"
    saver = Saver(database)
    saver.save(topic, data)

@main.command()
@click.argument('database', type=str)
@click.argument('mq', type=str)
def save_cli(database, mq):
    with open(path, 'r') as file:
        data = file.read()
    saver = Saver(database)
    saver.save(topic, data)

   
def make_mongodb_saver(f):
    #host, port = f.host, f.port
    client = pymongo.MongoClient(host=f.host, port=f.port)
    db = client.db
    users = db.users
    snapshots = db.snapshots

    def save_user(user_data):
        user_data = json.loads(user_data) 
        if users.find_one({'user_id':user_data['user_id']}):
            return
        user_data['snapshots'] = []
        age_epoch = user_data['birthday']
        user_data['birthday'] = datetime.datetime.fromtimestamp(age_epoch)
        print(f"saver- save_user: {user_data}")
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
        if topic == 'user':
            save_user(data)
            return

        data = json.loads(data)
        print(f"saver- save: {data[topic]}")
        datetime = datetime.datetime.fromtimestamp(data['datetime'])
        user_id = data['user_id']
        #find if there's a snapshot with the given timestamp. If not, create one.
        snap = snapshots.find_one({'user_id':user_id,'datetime':datetime})
        if not user:
            snap = {'datetime':datetime}
            users.update_one({'user_id':user_id}, {'$push':{'snapshots':datetime}})
            snapshots.insert_one({'user_id':user_id, 'datetime':datetime})

        #update entry
        snapshots.update_one({'user_id':user_id,'datetime':datetime},
            {'$set':data['topic']})

    return save

SAVER_SETUPS = {'mongodb': make_mongodb_saver}