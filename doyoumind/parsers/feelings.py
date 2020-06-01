import json


def parse_feelings(context, snapshot):
    '''
    Parses the feelings from the snapshot.
    (returns a json subobject containing the feelings data)

    :param context: the context object representing the folders
    :type context: utils.Context
    :param snapshot: the snapshot data to be parsed (in json format)
    :type snapshot: str
    :return: the result of the parser (in json format)
    :rtype: str
    '''
    snap_dict = json.loads(snapshot)
    result = {}
    result['feelings'] = snap_dict['feelings']
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'feelings'
    result['datetime'] = snap_dict['datetime']

    return json.dumps(result)


parse_feelings.fields = ['feelings']
