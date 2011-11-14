'''Base datastore class
'''
from ..util import Singleton


class BaseDatastore(Singleton):
    '''Base datastore class - singleton defines get and set methods
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''Get an instance or create the new one
        '''
        if not cls._instance:
            cls._instance = super(BaseDatastore, cls).__new__(cls, *args,
                                                              **kwargs)
        return cls._instance

    @classmethod
    def get_datastore(cls, backend):
        '''Get the datastore from backend configuration
        '''
        module = __import__(backend['DATASTORE'], globals(), locals(),
                            'Datastore')
        datastore_class = getattr(module, 'Datastore')
        return datastore_class(backend)


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
