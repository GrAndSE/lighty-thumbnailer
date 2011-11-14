BACKENDS = {
        'default': {
            'ENGINE': 'lighty.thumbnailer.engine.pil',
            'DATASTORE': 'lighty.thumbnailer.datastore.pyredis',
            'PREFFIX': 'thumbnail-default',
            'MEDIA_URL': 'media',
            'FORMAT': 'jpg',
        },
        'opaque': {
            'ENGINE': 'lighty.thumbnailer.engine.pgmagick',
            'DATASTORE': 'lighty.thumbnailer.datastore.redis',
            'PREFFIX': 'thumbnail-opaque',
            'MEDIA_URL': 'media',
            'FROMAT': 'png',
        }
}
