from lighty.thumbnailer import conf
from lighty.thumbnailer import image

print image.Thumbnail(conf.BACKENDS['default'], 'tests/imgs/test.jpg', 
                        (150, 150), ((0, 'px'), (0, 'px'), (0, 'px')), 
                        'both', ('top', 'left'), 'jpg').path
