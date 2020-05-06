import json

def parse_feelings(context, snapshot):
    print("invocating parse_feelings")
    snap_dict = json.loads(snapshot)
    result = {}
    result['feelings'] = snap_dict['feelings']
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'feelings' 
    result['datetime'] = snap_dict['datetime']

    #context.save('feelings.json', json.dumps(feelings_dict))
    return json.dumps(result)

parse_feelings.fields = ['feelings']