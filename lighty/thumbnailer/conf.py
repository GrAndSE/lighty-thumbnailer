BACKENDS = {
        'default': {
            'ENGINE': 'lighty.thumbnailer.engines.pil',
            'STORAGE': 'lighty.thumbnailer.storage.redis',
            'PREFFIX': 'thumbnail-default-',
        },
        'opaque': {
            'ENGINE': 'lighty.thumbnailer.engines.pgmagick',
            'STORAGE': 'lighty.thumbnailer.storage.redis',
            'PREFFIX': 'thumbnail-opaque-'
        }
}
