from PIL import Image 

def parse_depth_image(context, snapshot):
    path = context.path('depth_image.jpg')
    size = snapshot.depth_image.width, snapshot.depth_image.height
    image = Image.new('L', size)
    img_data = snapshot.depth_image.data
    if type(img_data) != bytes:
        floatlist = list(img_data)
        img_data = struct.pack('%sf' % len(floatlist), *floatlist)
    image.putdata(img_data)
    image.save(path) 

parse_depth_image.field = 'depth_image'

