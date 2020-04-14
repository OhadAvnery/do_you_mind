from PIL import Image 

def parse_color_image(context, snapshot):
    path = context.path('color_image.jpg')
    #size = snapshot.color_image.height, snapshot.color_image.width
    size = snapshot.color_image.width, snapshot.color_image.height
    #print(size)

    image = Image.new('RGB', size)
    print(f"size: {size}, actual data size (in bytes): {len(snapshot.color_image.data)}")
    image.putdata(snapshot.color_image.data)
    image.save(path) 

parse_color_image.field = 'color_image'

