MEDIA_ROOT = 'tests/imgs'
MEDIA_URL = 'test.com/media'

THUMBNAIL_DEBUG = False

INSTALLED_APPS = (
    'lighty.thumbnailer.integration.django',
)

THUMBNAILER_BACKENDS = {
    'django': {
        'MEDIA_ROOT': 'tests/imgs/',
        'MEDIA_URL': MEDIA_URL,
        'PREFFIX': 'thumbnailer-django',
    },
}
