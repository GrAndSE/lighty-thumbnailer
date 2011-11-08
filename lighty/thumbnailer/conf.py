BACKENDS = {
        'default': {
            'ENGINE': 'lighty.thumbnailer.engine.pil',
            'STORAGE': 'lighty.thumbnailer.storage.pyredis',
            'PREFFIX': 'thumbnail-default',
            'MEDIA_URL': 'media',
            'FORMAT': 'jpg',
        },
        'opaque': {
            'ENGINE': 'lighty.thumbnailer.engine.pgmagick',
            'STORAGE': 'lighty.thumbnailer.storage.redis',
            'PREFFIX': 'thumbnail-opaque',
            'MEDIA_URL': 'media',
            'FROMAT': 'png',
        }
}
