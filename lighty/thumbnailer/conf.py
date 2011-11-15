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
    FILTERS = ''


BACKENDS = {
    'default': {
        'ENGINE': 'lighty.thumbnailer.engine.pil',
        'FORMAT': 'jpg',
        'DATASTORE': 'lighty.thumbnailer.datastore.pyredis',
        'MEDIA_URL': 'media',
        'MEDIA_ROOT': 'media',
        'PREFFIX': 'thumbnail-default',
        'STORAGE': 'lighty.thumbnailer.storage.file',
    },
    'opaque': {
        'ENGINE': 'lighty.thumbnailer.engine.pgmagick',
        'FROMAT': 'png',
        'DATASTORE': 'lighty.thumbnailer.datastore.redis',
        'MEDIA_URL': 'media',
        'MEDIA_ROOT': 'media',
        'PREFFIX': 'thumbnail-opaque',
        'STORAGE': 'lighty.thumbnailer.storage.file',
    }
}
