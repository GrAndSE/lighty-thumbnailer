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


class InstanceForClass(Singleton):
    '''Class contains method
    '''

    @classmethod
    def get_instance(cls, backend):
        '''Get storage for backend
        '''
        module = __import__(backend[cls._param_name], globals(), locals(),
                            cls._class_name)
        storage_class = getattr(module, cls._class_name)
        return storage_class(backend)
