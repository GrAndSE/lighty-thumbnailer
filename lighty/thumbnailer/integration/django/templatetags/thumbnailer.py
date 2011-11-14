import re
import sys
import traceback

from django.conf import settings
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str

from lighty.thumbnailer.conf import BACKENDS
from lighty.thumbnailer.image import Thumbnail
from lighty.thumbnailer.utils import parse_size, parse_crop, parse_look

register = Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


class ThumbnailNodeBase(Node):
    """
    A Node that renders safely
    """
    nodelist_empty = NodeList()

    def render(self, context):
        try:
            return self._render(context)
        except Exception:
            if settings.THUMBNAIL_DEBUG:
                raise
            #logger.error('Thumbnail tag failed:', exc_info=sys.exc_info())
            traceback.print_exc(file=sys.stderr)
            return self.nodelist_empty.render(context)

    def _render(self, context):
        raise NotImplemented()


class ThumbnailNode(ThumbnailNodeBase):
    child_nodelists = ('nodelist_file', 'nodelist_empty')
    error_msg = ('Syntax error. Expected: ``thumbnail source geometry '
                 '[key1=val1 key2=val2...] as var``')

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 5 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)
        self.file_ = parser.compile_filter(bits[1])
        self.options = [('geometry', parser.compile_filter(bits[2]))]
        for bit in bits[3:-2]:
            m = kw_pat.match(bit)
            if not m:
                raise TemplateSyntaxError(self.error_msg)
            key = smart_str(m.group('key'))
            expr = parser.compile_filter(m.group('value'))
            self.options.append((key, expr))
        self.as_var = bits[-1]
        self.nodelist_file = parser.parse(('empty', 'endthumbnail',))
        if parser.next_token().contents == 'empty':
            self.nodelist_empty = parser.parse(('endthumbnail',))
            parser.delete_first_token()

    def _render(self, context):
        file_ = self.file_.resolve(context)
        options = {
            'crop': '0px 0px 0px 0px',
            'backend': 'default',
            'geometry': '0x0',
            'look': 'top left',
            'overflow': 'none',
            'filters': '',
            'format': 'jpg',
        }
        resolved = dict([(name, expr.resolve(context))
                         for name, expr in self.options])
        options.update(resolved)
        print resolved, '\n\n', options
        if file_:
            thumbnail = Thumbnail(
                    source_path=file_,
                    backend=BACKENDS[options['backend']],
                    geometry=parse_size(options['geometry']),
                    crop=parse_crop(options['crop']),
                    overflow=options['overflow'],
                    look=parse_look(options['look']),
                    format=options['format'],
            )
        else:
            return self.nodelist_empty.render(context)
        context.push()
        context[self.as_var] = thumbnail
        output = self.nodelist_file.render(context)
        context.pop()
        return output

    def __repr__(self):
        return "<ThumbnailNode>"

    def __iter__(self):
        for node in self.nodelist_file:
            yield node
        for node in self.nodelist_empty:
            yield node


@register.tag
def thumbnail(parser, token):
    return ThumbnailNode(parser, token)
