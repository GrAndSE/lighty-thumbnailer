from .conf import BACKENDS
from .image import Thumbnail
from .utils import parse_crop, parse_fit, parse_look, parse_size

FROM_BACKEND = ('filters', 'look', 'overflow', 'fit', 'quality', 'format', )

default_options = {
    'crop': '0px 0px 0px 0px',
    'backend': 'default',
    'geometry': '0x0',
}


def make_thumbnail(**args):
    backend_name = args['backend'] if 'backend' in args else 'default'
    backend = BACKENDS[backend_name]
    options = default_options.copy()
    options.update(dict([(opt, backend[opt.upper()]) for opt in FROM_BACKEND]))
    options.update(args)
    return Thumbnail(
                source_path=options['source_path'],
                backend=backend,
                geometry=parse_size(options['geometry']),
                crop=parse_crop(options['crop']),
                overflow=options['overflow'],
                look=parse_look(options['look']),
                fit=parse_fit(options['fit']),
                format=options['format'],
            )
