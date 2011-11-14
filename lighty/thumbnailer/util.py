'''Util classes and functions can be used in other utils
'''

class Singleton(object):
    '''Singleton class implementation
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''Get an instance or create the new one
        '''
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
