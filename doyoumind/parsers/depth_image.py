#from PIL import Image 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from utils.plt_utils import heatmap, annotate_heatmap

"""def parse_depth_image(context, snapshot):
    path = context.path('depth_image.jpg')
    size = snapshot.depth_image.width, snapshot.depth_image.height
    image = Image.new('L', size)
    img_data = snapshot.depth_image.data
    if type(img_data) != bytes:
        floatlist = list(img_data)
        img_data = struct.pack('%sf' % len(floatlist), *floatlist)
    image.putdata(img_data)
    image.save(path) """

def parse_depth_image(context, snapshot):
    #print("parse_depth_image: starting...")
    path = context.path('depth_image.jpg')
    float_vals = list(snapshot.depth_image.data)
    w, h = snapshot.depth_image.width, snapshot.depth_image.height
    float_matrix = []
    for i in range(h):
        float_matrix.append(float_vals[w*i : w*(i+1)])
    float_np = np.array(float_matrix)
    im = plt.imshow(float_np)
    plt.savefig(path)

    """fig, ax = plt.subplots()

    im, cbar = heatmap(float_np, [], [], ax=ax,
                   cmap="YlGn", cbarlabel="distance of object")
    texts = annotate_heatmap(im, valfmt="{x:.1f}")

    fig.tight_layout()
    #plt.show()
    print("parse_depth_image: there you go!")
    fig.save(path)"""


parse_depth_image.fields = ['depth_image']

