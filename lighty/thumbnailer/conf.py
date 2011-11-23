'''Configuration
'''

class defaults:
    DATASTORE = 'lighty.thumbnailer.datastore.pyredis'
    ENGINE = 'lighty.thumbnailer.engine.pil'
    STORAGE = 'lighty.thumbnailer.storage.file'
    MEDIA_URL = 'media'
    MEDIA_ROOT = 'media'
    PREFFIX = 'thumbnails'
    FORMAT = 'jpg'
    QUALITY = '95'
    LOOK = 'middle center'
    OVERFLOW = 'none'
    FIT = True
    FILTERS = ''


default_backend = defaults.__dict__.copy()
del default_backend['__doc__']
del default_backend['__module__']

BACKENDS = {'default': default_backend.copy()}
