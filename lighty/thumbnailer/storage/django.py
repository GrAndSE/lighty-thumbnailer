'''Django storage integration
'''

from django.core.files.storage import default_storage

from . import BaseStorage


class Storage(BaseStorage):
    '''Storage class for djang integration
    '''

    def open(self, path, mode='rb'):
        '''Open path as file object
        '''
        return default_storage.open(path, mode)

    def save(self, path, content):
        '''Save data into file
        '''
        default_storage.save(path, content)

    def exists(self, path):
        '''Check is file exists
        '''
        return default_storage.exists(path)
