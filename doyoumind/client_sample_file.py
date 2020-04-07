import os
from PIL import Image
import struct

from readers.reader import Reader

#SAMPLE_PATH = "/home/user/Downloads/sample.mind"
#SAVE_PATH = "/home/user/User_Thoughts_bin"

SAMPLE_PATH = "/home/user/Downloads/sample.mind.gz"
SAVE_PATH = "/home/user/User_Thoughts_protobuf"

#img_type - 'c' (color) or 'd' (depth)
def create_image(reader_image, img_type):
    img_vals = reader_image.data
    if img_type == 'c':
        img_fmt = "RGB"
    else:
        img_fmt = "L"
        #if img_vals is not a bytes object (but a float list), we explicitly convert it to bytes first.
        if type(img_vals) != bytes:
            floatlist = list(img_vals)
            img_vals = struct.pack('%sf' % len(floatlist), *floatlist)

    return Image.frombytes(img_fmt, (reader_image.width, reader_image.height), img_vals)


def load_sample(sample_path, save_path, format, zipped):
    read = Reader(sample_path, format, zipped)
    user = read.read_user()
    new_path = f"{save_path}/{user.user_id}"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for snap in read:
        filename = f"color image by {user.username} at {snap.datetime}"
        img_path = f"{new_path}/{filename}.jpg"
        created_color_image = create_image(snap.color_image, 'c')
        created_color_image.save(img_path)

        filename = f"depth image by {user.username} at {snap.datetime}"
        img_path = f"{new_path}/{filename}.jpg"
        #print(type(snap.depth_image.data))
        created_depth_image = create_image(snap.depth_image, 'd')
        created_depth_image.save(img_path)


if __name__ == "__main__":
    load_sample(SAMPLE_PATH, SAVE_PATH, 'protobuf', True)
    #load_sample(SAMPLE_PATH, SAVE_PATH, 'binary', False)

