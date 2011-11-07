class BaseImage(object):
    '''Wrapper around image file
    '''

    def __init__(self, path):
        '''Path to file work with
        '''
        self.path = path

    @classmethod
    def create(cls, backend, path):
        '''Create instance of image class from specified backend associated 
        with specified path
        '''
        module = __import__(backend['ENGINE'], globals(), locals(), 'Image')
        image_class = getattr(module, 'Image')
        return image_class(path)

    def save():
        '''Save to file
        '''
        pass

    def _read(self):
        '''Read file object
        '''
        raise NotImplemented('_read not implemented')

    def _write(self):
        '''Write to file
        '''
        raise NotImplemented('_write not implemented')


class Thumbnail(object):
    '''Image class used to store data
    '''

    def __init__(self, backend, source_path, geometry, crop, overflow, look):
        '''Create new image instance
        '''
        super(Thumbnail, self).__init__()
        self.backend = backend
        self.source = BaseImage.create(backend, source_path)
        self.geometry = geometry
        self.overflow = overflow
        self.crop = crop
        self.look = look
