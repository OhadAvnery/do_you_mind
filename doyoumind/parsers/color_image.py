import json 
import os
from PIL import Image

def parse_color_image(context, snapshot):
    print("invocating parse_color_image")
    path = context.path('color_image.jpg')
    snap_dict = json.loads(snapshot)
    size = snap_dict['color_image']['width'], snap_dict['color_image']['height']
    #image = Image.new('RGB', size)
    #image.putdata(snapshot.color_image.data)
    raw_file = snap_dict['color_image']['data']
    with open(raw_file, 'rb') as f:
        image_data = f.read()

    image = Image.frombytes('RGB', size, image_data)
    image.save(path) 

    #os.remove(raw_file) #return it back later!!!!



parse_color_image.fields = ['color_image']

