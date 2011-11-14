'''Filesystem storage
'''
import os

from . import BaseStorage


class Storage(BaseStorage):
    '''Class for storing file on a local file system
    '''

    def open(self, path, mode='rb'):
        '''Open file for reading
        '''
        return open(path, mode)

    def save(self, path, content):
        '''Save content to path
        '''
        dirs, name = path.rsplit('/', 1)
        directory = os.path.join(self.backend['MEDIA_ROOT'], dirs)
        if not os.path.exists(directory):
            os.makedirs(directory)
        out = open(os.path.join(directory, name), 'w')
        out.write(content)

    def size(self, path):
        '''Get size of the content located
        '''
        raise NotImplementedError('size was not implemented for class %s' %
                                  self.__class__.__name__)

    def list(self, path):
        '''Get list of files located
        '''
        return os.listdir(path)
 
    def exists(self, path):
        '''Check is path exists
        '''
        return os.path.exists(path)

    def delete(self, path):
        '''Delete file from storage
        '''
        raise NotImplementedError('delete was not implemented for class %s' %
                                  self.__class__.__name__)
