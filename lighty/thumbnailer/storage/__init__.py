'''Package contains the storage system
'''
from ..util import InstanceForClass, Singleton


class BaseStorage(InstanceForClass, Singleton):
    '''Base class for any storage
    '''

    def __init__(self, backend):
        '''Create new BaseStorage instance
        '''
        self.backend = backend

    def open(self, path, mode='rb'):
        '''Open file for reading
        '''
        raise NotImplementedError('open was not implemented for class %s' %
                                  self.__class__.__name__)

    def save(self, path, content):
        '''Save content to path
        '''
        raise NotImplementedError('save was not implemented for class %s' %
                                  self.__class__.__name__)

    def size(self, path):
        '''Get size of the content located
        '''
        raise NotImplementedError('size was not implemented for class %s' %
                                  self.__class__.__name__)

    def list(self, path):
        '''Get list of files located
        '''
        raise NotImplementedError('list was not implemented for class %s' %
                                  self.__class__.__name__)
 
    def exists(self, path):
        '''Check is path exists
        '''
        raise NotImplementedError('exists was not implemented for class %s' %
                                  self.__class__.__name__)

    def delete(self, path):
        '''Delete file from storage
        '''
        raise NotImplementedError('delete was not implemented for class %s' %
                                  self.__class__.__name__)
