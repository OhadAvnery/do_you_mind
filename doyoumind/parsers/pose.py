import json

def parse_pose(context, snapshot):
    print("invocating parse_pose")
    snap_dict = json.loads(snapshot)
    result = {}
    #print(f"parse_pose- our dict is: {snap_dict}")
    result['pose'] = snap_dict['pose']
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'pose' 
    result['datetime'] = snap_dict['datetime']

    #context.save('feelings.json', json.dumps(feelings_dict))
    return json.dumps(result)

parse_pose.fields = ['pose']