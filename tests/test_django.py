import os

from lighty.thumbnailer import conf
from lighty.thumbnailer import image

try:
    os.environ['DJANGO_SETTINGS_MODULE'] =  'tests.django_settings'
    from django.template import Context, Template
    import lighty.thumbnailer.integration.django

    test_backend = conf.BACKENDS['django']
    print image.Thumbnail(test_backend, 'test.jpg', (150, 150),
                          ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                          'both', ('top', 'left'), 'jpg').url
    print image.Thumbnail(test_backend, 'test.jpg', (150, 150), 
                          ((30, 'px'), (30, 'px'), (45, 'px'), (50, 'px')),
                          'both', ('top', 'left'), 'jpg').url
    print "-----"
    print 60, 80, 'overflow-x', 'top', 'center'
    print image.Thumbnail(test_backend, 'tests.jpg', (60, 80),
                          ((0, 'px'), (0, 'px'), (0, 'px'), (0, 'px')),
                          'x', ('top', 'center'), 'jpg').url, "\n"
    print 156, 255, 'overflow-x', 'middle', 'right'
    print image.Thumbnail(test_backend, 'tests.jpg', (156, 255),
                          ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                          'x', ('middle', 'right'), 'jpg').url, "\n"
    print 309, 464, 'overflow-y', 'bottom', 'center'
    print image.Thumbnail(test_backend, 'tests.jpg', (309, 464),
                          ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                          'y', ('bottom', 'center'), 'jpg').url, "\n"
    print 400, 600, 'none', 'middle', 'center'
    print image.Thumbnail(test_backend, 'tests.jpg', (400, 600),
                          ((15, '%'), (0, 'px'), (0, 'px'), (0, 'px')),
                          'none', ('middle', 'center'), 'jpg').url, "\n"

    template = Template('''{% load thumbnailer %}
    {% thumbnailer image "400x600" backend="django" crop="15% 0px 0px 0px" overflow="none" loot="middle center" format="jpg" as thumb %}
        {{ thumb.path }} 
        {{ thumb.url }}
    {% endthumbnail %}
    ''')
    print template.render(Context({'image': 'tests.jpg'}))
except ImportError as e:
    import sys
    import traceback
    print traceback.print_exc(file=sys.stdout)
