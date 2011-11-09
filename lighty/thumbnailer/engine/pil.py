from PIL import Image as PILImage

from lighty.thumbnailer.image import BaseImage


FORMATS = {
        'jpg': 'jpeg',
        'png': 'png',
}


class Image(BaseImage):
    '''Base image class
    '''

    def __init__(self, backend, path=None, image=None):
        '''Create an image instance
        '''
        super(Image, self).__init__(backend, path, image)

    def _read(self, path):
        '''Read file
        '''
        self.image = PILImage.open(path)

    def _write(self, path, extension):
        '''Save into file
        '''
        if extension not in FORMATS:
            raise ValueError('Unsupported file extension')
        self.image.save(path, FORMATS[extension])

    def _size(self):
        '''Get the image size
        '''
        if self.image is None:
            self._read(self.full_path())
        return self.image.size

    def _crop(self, top_crop, left_crop, bottom_crop, right_crop):
        width, height = self.image.size
        return self.image.crop((left_crop, top_crop,
                                width - right_crop, height - bottom_crop))
