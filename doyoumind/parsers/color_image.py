import json
import os
from PIL import Image


def parse_color_image(context, snapshot):
    '''
    Parses the color image from the snapshot.
    (deletes the raw data file and writes to disk
    a jpg file representing the color image.
    Uses PIL. Returns the image's path.)

    :param context: the context object representing the folders
    :type context: utils.Context
    :param snapshot: the snapshot data to be parsed (in json format)
    :type snapshot: str
    :returns: the result of the parser (in json format)
    :rtype: str
    '''
    path = context.path('color_image.jpg')
    snap_dict = json.loads(snapshot)
    size = snap_dict['color_image']['width'], snap_dict['color_image']['height']
    raw_file = snap_dict['color_image']['data']
    with open(raw_file, 'rb') as f:
        image_data = f.read()

    image = Image.frombytes('RGB', size, image_data)
    image.save(path)

    os.remove(raw_file)
    result = {}
    result['color_image'] = path.as_posix()
    result['user_id'] = snap_dict['user_id']
    result['parser'] = 'color_image'
    result['datetime'] = snap_dict['datetime']
    return json.dumps(result)


parse_color_image.fields = ['color_image']
