import os
from PIL import Image as PILImage

from lighty.thumbnailer.image import BaseImage


class Image(BaseImage):
    '''Base image class
    '''

    def __init__(self, path=None, image=None):
        '''Create an image instance
        '''
        self.path = path
        if path is not None and os.path.exists(path):
            self.image = self._read()
        else:
            self.image = image

    def _read(self):
        '''Read file
        '''
        self.image = PILImage.open(self.path)

    def _write(self, format='jpeg'):
        '''Save into file
        '''
        self.image.save(self.path, format)

    def _size(self):
        '''Get the image size
        '''
        if self.image is None:
            self._read()
        return self.image.size

    def _crop(self, top_crop, left_crop, bottom_crop, right_crop):
        width, height = self.image.size
        return self.image.crop((top_crop, left_crop,
                                height - bottom_crop, width - right_crop))
