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
        self.storage = BaseStorage.get_instance(backend)
        if path is not None:
            self.open(force=False)

    @classmethod
    def create(cls, backend, path):
        '''Create instance of image class from specified backend associated
        with specified path
        '''
        return cls.get_instance(backend, path)

    @classmethod
    def thumbnail(cls, backend, source_path, geometry, crop, overflow, look,
                  fit):
        image = cls.create(backend, source_path)
        image = image.crop(crop)
        return image.scale(geometry, overflow, look, fit)

    def full_path(self, path=None):
        '''Get full path to file
        '''
        file_path = path or self.path
        if file_path.startswith('/'):
            return file_path
        else:
            return os.path.join(self.backend['MEDIA_ROOT'], file_path)

    def open(self, path=None, force=True):
        '''Read file from path specified or self.path
        '''
        full_path = self.full_path(path)
        if force or self.storage.exists(full_path):
            self._read(self.storage.open(full_path))

    def save(self):
        '''Save to file
        '''
        extension = self.path.rsplit('.', 1)[1]
        out = StringIO.StringIO()
        self._write(out, extension)
        self.storage.save(self.path, out.getvalue())
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

    def scale(self, geometry, overflow, look, fit):
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
                bottom_crop = diff_y
            elif look[0] == 'bottom':
                top_crop = diff_y
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
                if fit:
                    if original_ratio > to_ratio:
                        scale = float(to_height) / original_height
                        to = float(to_height) * original_ratio
                        diff_x = int((to - to_width) / scale)
                        diff_y = 0
                    else:
                        diff_x = 0
                        scale = float(to_width) / original_width
                        to = float(to_width) / original_ratio
                        diff_y = int((to - to_height) / scale)
                else:
                    if to_height < original_height:
                        diff_x = original_width - to_width
                        diff_y = original_height - to_height
                    else:
                        diff_x = original_width - int(original_height /
                                                      to_ratio)
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

    @property
    def width(self):
        '''Get image height
        '''
        return self._size()[0]

    @property
    def height(self):
        '''Get image width
        '''
        return self._size()[1]


class Thumbnail(object):
    '''Image class used to store data
    '''
    __slots__ = ('backend', 'source', 'geometry', 'crop', 'overflow', 'look',
                 'fit', 'format', 'image', '_key', 'storage', 'datastore', 
                 'width', 'height', 'url', 'path', '_get_path', '_get_key',
                 '_gen_path', '_get_image')

    def __init__(self, backend, source_path, geometry, crop, overflow, look, 
                 fit=True, format='jpg'):
        '''Create new image instance
        '''
        super(Thumbnail, self).__init__()
        # Options
        self.backend = backend
        self.source = BaseImage.create(backend, source_path)
        self.geometry = geometry
        self.overflow = overflow
        self.crop = crop
        self.look = look
        self.fit = fit
        self.format = format
        self.image = None
        self._key = None
        # Datastore, storage, etc. initialization
        self.storage = BaseStorage.get_instance(backend)
        self.datastore = BaseDatastore.get_instance(backend)

    def _get_key(self):
        '''Get datastore key
        '''
        if self._key:
            return self._key
        source_hash = hashlib.sha1(self.source.path).hexdigest()
        crop = tuple([str(c[0]) + (c[1] == '%' and 'pc' or c[1])
                      for c in self.crop])
        option_hash = '-'.join([str(i) for i in self.geometry + crop + 
                                self.look] + 
                                [self.overflow, str(self.fit), self.format])
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
        path = self.datastore.get(key)
        if path is not None:
            full_path = os.path.join(self.backend['MEDIA_ROOT'], path)
            if self.storage.exists(full_path):
                return BaseImage.create(self.backend, path)
        # Create new image and store the data
        self.image = BaseImage.thumbnail(self.backend, self.source.path,
                                         self.geometry, self.crop,
                                         self.overflow, self.look, self.fit)
        path = self._gen_path()
        self.image.path = path
        self.image.save()
        self.datastore.set(key, path)
        return self.image

    @property
    def width(self):
        '''Get thumbnail width
        '''
        if self.image is None:
            return self._get_image().width
        return self.image.width

    @property
    def height(self):
        '''Get thumbnail width
        '''
        if self.image is None:
            return self._get_image().height
        return self.image.height

    @property
    def url(self):
        return "%s/%s" % (self.backend['MEDIA_URL'],  self._get_path())

    @property
    def path(self):
        return self._get_path()
