'''Base datastore class
'''
from ..util import InstanceForClass


class BaseDatastore(InstanceForClass):
    '''Base datastore class - singleton defines get and set methods
    '''
    _class_name = 'Datastore'
    _param_name = 'DATASTORE'

    @classmethod
    def get_datastore(cls, backend):
        '''Get the datastore from backend configuration
        '''
        return cls.get_instance(backend)


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
