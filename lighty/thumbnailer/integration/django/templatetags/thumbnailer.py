import re
import sys
import traceback

from django.conf import settings
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str

from lighty.thumbnailer.helpers import make_thumbnail

register = Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


class ThumbnailNode(Node):
    '''Node makes thumbnail
    '''
    nodelist_empty = NodeList()
    child_nodelists = ('nodelist_file', 'nodelist_empty')
    error_msg = ('Syntax error. Expected: ``thumbnailer source_path geometry '
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

    def render(self, context):
        try:
            return self._render(context)
        except Exception:
            if settings.THUMBNAIL_DEBUG:
                raise
            traceback.print_exc(file=sys.stderr)
            return self.nodelist_empty.render(context)

    def _render(self, context):
        '''Inner template node rendering
        '''
        # Get arguments
        file_ = self.file_.resolve(context)
        if file_ is None or file_ == 'None':
            raise ValueError('Null source image')
        if not isinstance(file_, basestring):
            file_ = unicode(file_)
        resolved = dict([(name, expr.resolve(context))
                         for name, expr in self.options])
        resolved['source_path'] = file_
        # Generate thumbnail
        if file_:
            thumbnail = make_thumbnail(**resolved)
        else:
            return self.nodelist_empty.render(context)
        # Puh context`
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
def thumbnailer(parser, token):
    return ThumbnailNode(parser, token)
