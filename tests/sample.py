from lighty.thumbnailer import conf
from lighty.thumbnailer import image

test_backend = {}
test_backend.update(conf.BACKENDS['default'])
test_backend['MEDIA_ROOT'] = 'tests/imgs/'
print image.Thumbnail(test_backend, 'test.jpg',
                      (150, 150), ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'both', ('top', 'left'), 'jpg').path
print image.Thumbnail(test_backend, 'test.jpg', (150, 150), 
                      ((30, 'px'), (30, 'px'), (45, 'px'), (50, 'px')),
                      'both', ('top', 'left'), 'jpg').path
