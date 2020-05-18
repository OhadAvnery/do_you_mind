from .api_mongodb import APIMongoDB
DRIVERS = {'mongodb': APIMongoDB}

LARGE_DATA_FIELDS = {'depth_image', 'color_image'}