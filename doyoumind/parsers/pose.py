import json


def parse_pose(context, snapshot):
    '''
    Parses the pose from the snapshot.
    (returns a json subobject containing the translation+rotation data)

    :param context: the context object representing the folders
    :type context: utils.Context
    :param snapshot: the snapshot data to be parsed (in json format)
    :type snapshot: str
    :return: the result of the parser (in json format)
    :rtype: str
    '''
    snap_dict = json.loads(snapshot)
    result = {}
    result['pose'] = snap_dict['pose']
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'pose'
    result['datetime'] = snap_dict['datetime']

    return json.dumps(result)


parse_pose.fields = ['pose']
