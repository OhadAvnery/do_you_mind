import json

def parse_feelings(context, snapshot):
    snap_dict = json.loads(snapshot)
    feelings_dict = snap_dict['feelings']
    context.save('feelings.json', json.dumps(feelings_dict))

parse_feelings.fields = ['feelings']