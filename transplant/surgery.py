'''
This module contains Surgery class.
'''
import importlib

from django.core.exceptions import ImproperlyConfigured

class Surgery:
    '''
    This class initializes proper Manager and Surgeon basing on given strings
    and kwargs. It also takes care of proper exception handling during the
    merge process.
    '''
    def __init__(self, model, surgeon, manager='objects', **kwargs):
        '''
        Initializes proper model and surgeon from given arguments, raising
        ImproperlyConfigured if manager or surgeon does not exist.
        '''
        modulepath, classname = self.split_path(model)
        try:
            models = importlib.import_module(modulepath)
            self.model = getattr(models, classname)
        except (ImportError, AttributeError):
            raise ImproperlyConfigured(
              "Could not import model '{0}' from module '{1}'.".format(
                  classname, modulepath)
            )
        try:
            self.manager = getattr(self.model, manager)
        except AttributeError:
            raise ImproperlyConfigured(
              "Model '{0}' does not have manager '{1}'.".format(classname, manager)
            )
        
        try:
            modulepath, classname = self.split_path(surgeon)
            surgeons = importlib.import_module(modulepath)
            surgeon_class = getattr(surgeons, classname)
        except (ImportError, AttributeError):
            raise ImproperlyConfigured(
              "Could not import surgeon '{0}' from module '{1}'.".format(
                  classname, modulepath)
            )
        self.surgeon = surgeon_class(self.manager, **kwargs)
    
    def split_path(self, modelpath):
        '''
        Splits 'model.path.ClassName' into ('model.path', 'ClassName')
        '''
        chunks = modelpath.split('.')
        classname = chunks.pop()
        modulepath = '.'.join(chunks)
        return (modulepath, classname)
    
    def merge(self, receiver, donor):
        self.surgeon.merge(receiver, donor)