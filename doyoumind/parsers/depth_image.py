#from PIL import Image 
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import touch



def parse_depth_image(context, snapshot):
    '''
    Parses the depth image from the snapshot.

    :param context: the context object representing the folders
    :type context: utils.Context
    :param snapshot: the snapshot data to be parsed (in json format)
    :type snapshot: str
    :return: the result of the parser (in json format)
    :rtype: str
    '''
    path = context.path('depth_image.jpg')
    snap_dict = json.loads(snapshot)
    w, h = snap_dict['depth_image']['width'], snap_dict['depth_image']['height']

    raw_file = snap_dict['depth_image']['data'] 
    float_vals = np.load(raw_file)

    float_matrix = []
    for i in range(h):
        float_matrix.append(float_vals[w*i : w*(i+1)])
    float_np = np.array(float_matrix)
    im = plt.imshow(float_np)
    touch.touch(path)
    plt.savefig(path)

    os.remove(raw_file)
    result = {}
    result['depth_image'] = path.as_posix()
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'depth_image'
    result['datetime'] = snap_dict['datetime']
    return json.dumps(result)



parse_depth_image.fields = ['depth_image']

