BACKENDS = {
        'default': {
            'ENGINE': 'lighty.thumbnailer.engine.pil',
            'FORMAT': 'jpg',
            'DATASTORE': 'lighty.thumbnailer.datastore.pyredis',
            'MEDIA_URL': 'media',
            'PREFFIX': 'thumbnail-default',
            'STORAGE': 'lighty.thumbnailer.storage.file',
        },
        'opaque': {
            'ENGINE': 'lighty.thumbnailer.engine.pgmagick',
            'FROMAT': 'png',
            'DATASTORE': 'lighty.thumbnailer.datastore.redis',
            'MEDIA_URL': 'media',
            'PREFFIX': 'thumbnail-opaque',
            'STORAGE': 'lighty.thumbnailer.storage.file',
        }
}
