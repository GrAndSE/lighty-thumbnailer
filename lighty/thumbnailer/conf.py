BACKENDS = {
        'default': {
            'ENGINE': 'lighty.thumbnailer.engine.pil',
            'STORAGE': 'lighty.thumbnailer.storage.redis',
            'PREFFIX': 'thumbnail-default',
        },
        'opaque': {
            'ENGINE': 'lighty.thumbnailer.engine.pgmagick',
            'STORAGE': 'lighty.thumbnailer.storage.redis',
            'PREFFIX': 'thumbnail-opaque'
        }
}
