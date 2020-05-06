import json

def parse_pose(context, snapshot):
    snap_dict = json.loads(snapshot)
    result = {}
    result['pose'] = snap_dict['pose']
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'pose' 
    result['datetime'] = snap_dict['datetime']

    #context.save('feelings.json', json.dumps(feelings_dict))
    return json.dumps(result)

parse_pose.fields = ['rotation', 'translation']