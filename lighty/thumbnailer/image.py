'''Classes used to wrap images and manipulate with images
'''
import hashlib


class BaseImage(object):
    '''Wrapper around image file
    '''

    def __init__(self, path=None, image=None):
        '''Path to file work with
        '''
        self.path = path
        self.image = image

    @classmethod
    def create(cls, backend, path):
        '''Create instance of image class from specified backend associated
        with specified path
        '''
        module = __import__(backend['ENGINE'], globals(), locals(), 'Image')
        image_class = getattr(module, 'Image')
        return image_class(path)

    @classmethod
    def thumbnail(cls, backend, source_path, geometry, crop, overflow, look):
        image = cls.create(backend, source_path).crop(crop)
        return image

    def save(self):
        '''Save to file
        '''
        raise NotImplemented('save not implemented')

    def _read(self):
        '''Read file object
        '''
        raise NotImplemented('_read not implemented')

    def _write(self):
        '''Write to file
        '''
        raise NotImplemented('_write not implemented')

    def _size(self):
        '''Get an image size
        '''
        raise NotImplemented('_size is not implemented')

    def crop(self, crop, geometry, overflow, scale):
        '''Crop image
        '''
        def get_crop_value(length, value, units):
            return units == 'px' and value or int(length * value / 100)
        width, height = self._size()
        top_crop = get_crop_value(height, *crop[0])
        left_crop = get_crop_value(width, *crop[1])
        bottom_crop = get_crop_value(height, *crop[2])
        right_crop = get_crop_value(width, *crop[3])
        image = self._crop(top_crop, left_crop, bottom_crop, right_crop)
        return self.__class__(image=image)

    def _crop(self, top_crop, left_crop, bottom_crop, right_crop):
        '''Library dependent crop
        '''
        raise NotImplemented('_crop not implemented')


class Thumbnail(object):
    '''Image class used to store data
    '''
    __slots__ = ('backend', 'source', 'geometry', 'crop', 'overflow', 'look',
                 'format', 'image', '_key')

    def __init__(self, backend, source_path, geometry, crop, overflow, look,
                 format):
        '''Create new image instance
        '''
        super(Thumbnail, self).__init__()
        self.backend = backend
        self.source = BaseImage.create(backend, source_path)
        self.geometry = geometry
        self.overflow = overflow
        self.crop = crop
        self.look = look
        self.format = format
        self.image = None
        self._key = None

    def _get_key(self):
        '''Get datastore key
        '''
        if self._key:
            return self._key
        source_hash = hashlib.sha1(self.source.path).hexdigest()
        crop = tuple([str(c[0]) + (c[1] == '%' and 'pc' or c[1])
                      for c in self.crop])
        option_hash = '-'.join([str(i) for i in self.geometry + crop +
                                self.look] + [self.overflow, self.format])
        self._key = '%s-%s-%s' % (self.backend['PREFFIX'], source_hash,
                                  option_hash)
        return self._key

    def _get_path(self):
        '''Get url for new file
        '''
        if not self.image:
            return self.image.path
        hash = hashlib.sha1(self._get_key()).hexdigest()
        return '%s/%s/%s.%s' % (hash[0:2], hash[2:4], hash[4:], self.format)

    def _get_image(self):
        '''Check datastore for image exists, chen check is image on specified
        path exists and if all ok return an image on path specified. Otherway
        create new image and return it
        '''
        key = self._get_key()
        #if 
        #path = 
        return None

    @property
    def url(self):
        return "%s/%s/%s" % (self.backend['MEDIA_URL'],
                             self.backend['PREFFIX'], self.image.path)
