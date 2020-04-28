from parsers.main_parser import MainParser, Context
#from server import SUPPORTED_FIELDS


SUPPORTED_FIELDS = ["translation", "rotation", "feelings", "color_image", "depth_image"]
#SUPPORTED_FIELDS = ["translation", "rotation", "feelings", "color_image"]

def publish_mq(mq_string, msg, context):
    print('cool function bro')
    main_parser = MainParser(SUPPORTED_FIELDS)
    main_parser.parse(context, msg)