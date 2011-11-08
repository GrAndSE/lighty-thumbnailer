import redis

from . import BaseStorage


class Storage(BaseStorage):
    '''Storage to get and put the data
    '''
    __slots__ = ('_instance', '__init__', 'connection', 'get', 'set', )

    def __init__(self, backend):
        '''Create new Storage instance
        '''
        self.connection = redis.Redis('localhost')  # TODO: get from backend

    def get(self, key):
        '''Get value for key
        '''
        return self.connection.get(key)

    def set(self, key, value):
        '''Set value for key
        '''
        self.connection.set(key, value)
