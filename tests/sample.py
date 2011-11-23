from lighty.thumbnailer import conf
from lighty.thumbnailer import image

test_backend = {}
test_backend.update(conf.BACKENDS['default'])
test_backend['MEDIA_ROOT'] = 'tests/imgs/'
print image.Thumbnail(test_backend, 'test.jpg', (150, 150),
                      ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'both', ('top', 'left'), True, 'jpg').path
print image.Thumbnail(test_backend, 'test.jpg', (150, 150), 
                      ((30, 'px'), (30, 'px'), (45, 'px'), (50, 'px')),
                      'both', ('top', 'left'), False, 'jpg').path
print "-----"
print 60, 80, 'overflow-x', 'top', 'center'
print image.Thumbnail(test_backend, 'tests.jpg', (60, 80),
                      ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'x', ('top', 'center'), False, 'jpg').path, "\n"
print 156, 255, 'overflow-x', 'middle', 'right'
print image.Thumbnail(test_backend, 'tests.jpg', (156, 255),
                      ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'x', ('middle', 'right'), False, 'jpg').path, "\n"
print 309, 464, 'overflow-y', 'bottom', 'center'
print image.Thumbnail(test_backend, 'tests.jpg', (309, 464),
                      ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'y', ('bottom', 'center'), False, 'jpg').path, "\n"
print 400, 600, 'none', 'middle', 'center'
print image.Thumbnail(test_backend, 'tests.jpg', (400, 600),
                      ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'none', ('middle', 'center'), False, 'jpg').path, "\n"
print 150, 150, 'both', 'middle', 'center'
print image.Thumbnail(test_backend, 'tests.jpg', (150, 150),
                      ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                      'both', ('middle', 'center'), True, 'jpg').path, "\n"
