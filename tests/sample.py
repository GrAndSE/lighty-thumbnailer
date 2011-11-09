from lighty.thumbnailer import conf
from lighty.thumbnailer import image

test_backend = {}
test_backend.update(conf.BACKENDS['default'])
test_backend['MEDIA_ROOT'] = 'tests/imgs/'
print image.Thumbnail(test_backend, 'tests/imgs/test.jpg',
                      (150, 150), ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'both', ('top', 'left'), 'jpg').path
