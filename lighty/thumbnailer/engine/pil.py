import os
from PIL import Image as PILImage

from lighty.thumbnailer.image import BaseImage


class Image(BaseImage):
    '''Base image class
    '''

    def __init__(self, path):
        '''Create an image instance
        '''
        self.path = path
        if os.path.exists(path):
            self.image = self._read()
        else:
            self.image = None

    def _read(self):
        '''Read file
        '''
        self.image = PILImage.open(self.path)

    def _write(self, format='jpg'):
        '''Save into file
        '''
        self.image.save(self.path, format)
