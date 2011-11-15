from .conf import defaults, BACKENDS
from .image import Thumbnail
from .utils import parse_crop, parse_look, parse_size

default_options = {
    'crop': '0px 0px 0px 0px',
    'backend': 'default',
    'geometry': '0x0',
    'filters': defaults.FILTERS,
    'look': defaults.LOOK,
    'overflow': defaults.OVERFLOW,
    'quality': defaults.QUALITY,
    'format': defaults.FORMAT,
}


def make_thumbnail(**args):
    options = default_options.copy()
    options.update(args)
    return Thumbnail(
                source_path=options['source_path'],
                backend=BACKENDS[options['backend']],
                geometry=parse_size(options['geometry']),
                crop=parse_crop(options['crop']),
                overflow=options['overflow'],
                look=parse_look(options['look']),
                format=options['format'],
            )
