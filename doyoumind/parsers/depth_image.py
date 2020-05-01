#from PIL import Image 
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import touch

from ..utils.plt_utils import heatmap, annotate_heatmap


def parse_depth_image(context, snapshot):
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


    """fig, ax = plt.subplots()

    im, cbar = heatmap(float_np, [], [], ax=ax,
                   cmap="YlGn", cbarlabel="distance of object")
    texts = annotate_heatmap(im, valfmt="{x:.1f}")

    fig.tight_layout()
    #plt.show()
    print("parse_depth_image: there you go!")
    fig.save(path)"""


parse_depth_image.fields = ['depth_image']

