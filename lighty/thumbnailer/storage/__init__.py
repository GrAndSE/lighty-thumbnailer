'''Base storage class
'''


class BaseStorage(object):
    '''Base storage class - singleton defines get and set methods
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseStorage, cls).__new__(cls, *args,
                                                            **kwargs)
        return cls._instance

    def get(self, key):
        '''Just raise because this method would be implemented in subclasses
        '''
        raise NotImplemented('get(key) was not implemented for %s' % 
                                self.__class__.__name__)

    def set(self, key, value):
        '''Just raise because this method would be implemented in subclasses
        '''
        raise NotImplemented('set(key, value) was not implemented for %s' % 
                                self.__class__.__name__)
