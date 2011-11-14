'''Classes used to wrap images and manipulate with images
'''
import hashlib
import os

try:
    import cStringIO as StringIO
except:
    import StringIO

from .datastore import BaseDatastore
from .storage import BaseStorage

from .util import InstanceForClass


class BaseImage(InstanceForClass):
    '''Wrapper around image file
    '''
    _param_name = 'ENGINE'
    _class_name = 'Image'

    def __init__(self, backend, path=None, image=None):
        '''Path to file work with
        '''
        self.path = path
        self.image = image
        self.backend = backend
        if path is not None:
            self.open(force=False)

    @classmethod
    def create(cls, backend, path):
        '''Create instance of image class from specified backend associated
        with specified path
        '''
        return cls.get_instance(backend, path)

    @classmethod
    def thumbnail(cls, backend, source_path, geometry, crop, overflow, look):
        image = cls.create(backend, source_path)
        image = image.crop(crop)
        return image.scale(geometry, overflow, look)

    def full_path(self, path=None):
        '''Get full path to file
        '''
        return os.path.join(self.backend['MEDIA_ROOT'], path or self.path)

    def open(self, path=None, force=True):
        '''Read file from path specified or self.path
        '''
        full_path = self.full_path(path)
        storage = BaseStorage.get_instance(self.backend)
        if force or storage.exists(full_path):
            self._read(storage.open(full_path))

    def save(self):
        '''Save to file
        '''
        extension = self.path.rsplit('.', 1)[1]
        out = StringIO.StringIO()
        self._write(out, extension)
        BaseStorage.get_instance(self.backend).save(self.path, out.getvalue())
        out.close()

    def _read(self):
        '''Read file object
        '''
        raise NotImplementedError('_read was not implemented for %s' % 
                                  self.__class__.__name__)

    def _write(self, path, extension):
        '''Write to file
        '''
        raise NotImplementedError('_write was not implemented for %s' % 
                                  self.__class__.__name__)

    def _size(self):
        '''Get an image size
        '''
        raise NotImplementedError('_size was not implemented for %s' % 
                                  self.__class__.__name__)

    def crop(self, crop):
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
        return self.__class__(self.backend, image=image)

    def _crop(self, top_crop, left_crop, bottom_crop, right_crop):
        '''Library dependent crop
        '''
        raise NotImplementedError('_crop was not implemented for %s' % 
                                  self.__class__.__name__)

    def scale(self, geometry, overflow, look):
        '''Scale the image including overflow and look
        '''
        def eval_crop(diff_x, diff_y):
            top_crop, left_crop, bottom_crop, right_crop = 0, 0, 0, 0
            if look[1] == 'left':
                right_crop = diff_x
            elif look[1] == 'right':
                left_crop = diff_x
            else:
                left_crop = right_crop = diff_x / 2
            if look[0] == 'top':
                top_crop = diff_y
            elif look[0] == 'bottom':
                bottom_crop = diff_y
            else:
                top_crop = bottom_crop = diff_y / 2
            return top_crop, left_crop, bottom_crop, right_crop
        # Get width, height and ratios
        original_width, original_height = self._size()
        to_width, to_height = geometry
        original_ratio = float(original_width) / original_height
        to_ratio = float(to_width) / to_height
        crop = (0, 0, 0, 0)
        width, height = to_width, to_height
        # Eval crops and ratio
        if original_ratio != to_ratio:
            if overflow == 'both':
                if to_height < original_height:
                    diff_x = original_width - to_width
                    diff_y = original_height - to_height
                else:
                    diff_x = original_width - int(original_height * to_ratio)
                    diff_y = 0
                crop = eval_crop(diff_x, diff_y)
            else:
                if original_ratio > to_ratio:
                    if overflow == 'x':
                        diff = original_width - int(original_height * to_ratio)
                        crop = eval_crop(diff, 0)
                    else:
                        width = to_width
                        height = int(width / original_ratio)
                else:
                    if overflow == 'y':
                        diff = int(original_height * to_ratio) - original_width
                        crop = eval_crop(0, diff)
                    else:
                        height = to_height
                        width = int(height * original_ratio)
        # Make crop if needed
        top_crop, left_crop, bottom_crop, right_crop = crop
        if top_crop or left_crop or bottom_crop or right_crop:
            source = self.crop(((top_crop, 'px'), (left_crop, 'px'), 
                                (bottom_crop, 'px'), (right_crop, 'px')))
        else:
            source = self
        image = source._scale(width, height)
        return self.__class__(self.backend, image=image)

    def _scale(self, width, height):
        '''Library dependent image scale
        '''
        raise NotImplementedError('_scale was not implemented for %s' % 
                                  self.__class__.__name__)


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

    def _gen_path(self):
        '''Get the path for new file
        '''
        hash = hashlib.sha1(self._get_key()).hexdigest()
        return "%s.%s" % (os.path.join(self.backend['PREFFIX'], hash[0:2],
                                       hash[2:4], hash[4:]),
                          self.format)

    def _get_path(self):
        '''Get relative path for new file
        '''
        if self.image is not None:
            return self.image.path
        return self._get_image().path

    def _get_image(self):
        '''Check datastore for image exists, chen check is image on specified
        path exists and if all ok return an image on path specified. Otherway
        create new image and return it
        '''
        # Check is value in datastorage and is path exists and could be read
        key = self._get_key()
        path = BaseDatastore.get_datastore(self.backend).get(key)
        if path is not None:
            if os.path.exists(os.path.join(self.backend['MEDIA_ROOT'], path)):
                return BaseImage.create(self.backend, path)
        # Create new image and store the data
        self.image = BaseImage.thumbnail(self.backend, self.source.path,
                                         self.geometry, self.crop,
                                         self.overflow, self.look)
        path = self._gen_path()
        self.image.path = path
        self.image.save()
        BaseDatastore.get_datastore(self.backend).set(key, path)
        return self.image

    @property
    def url(self):
        return "%s/%s/%s" % (self.backend['MEDIA_URL'],
                             self.backend['PREFFIX'], self._get_path())

    @property
    def path(self):
        return self._get_path()
