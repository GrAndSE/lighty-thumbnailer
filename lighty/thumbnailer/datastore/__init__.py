'''Base storage class
'''


class BaseStorage(object):
    '''Base storage class - singleton defines get and set methods
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''Get an instance or create the new one
        '''
        if not cls._instance:
            cls._instance = super(BaseStorage, cls).__new__(cls, *args,
                                                            **kwargs)
        return cls._instance

    @classmethod
    def get_storage(cls, backend):
        '''Get the storage frm backend configuration
        '''
        module = __import__(backend['STORAGE'], globals(), locals(), 'Storage')
        storage_class = getattr(module, 'Storage')
        return storage_class(backend)


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
