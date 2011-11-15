'''Integration with django settings
'''
from django.conf import settings

from lighty.thumbnailer import conf

for backend_name in settings.THUMBNAILER_BACKENDS:
    backend = settings.THUMBNAILER_BACKENDS[backend_name]
    conf.BACKENDS[backend_name] = conf.default_backend.copy()
    conf.BACKENDS[backend_name].update(backend)
