'''
This module contains Surgeon classes. Surgeon objects perform operation on
models' managers and user instances when performing an account merge.
'''

class NopSurgeon:
    '''
    This is a surgeon class that performs a 'merge' by doing nothing
    (it leaves the database unchanged).
    '''
    def __init__(self, manager, user_field='user'):
        self.user_field = user_field
        self.manager = manager

    def merge(self, receiver, donor):
        '''
        Merges two users. In this implementation this method does nothing.
        '''
        pass

class DefaultSurgeon(NopSurgeon):
    '''
    This class merges two users by setting user (or a field given as
    'user_field') to receiver on all objects in given manager and calling
    save() on each of them (so that all signals etc. are fired)
    '''
    
    def merge(self, receiver, donor):
        '''
        Sets donor.is_active to false.
        
        Iterates over given manager and changes 'user_field' field value
        to self.receiver. Calls save on each objects separately.
        '''
        if receiver is donor:
            return
        donor.is_active = False
        donor.save()
        
        kw = {'{0}'.format(self.user_field): donor}
        for obj in self.manager.filter(**kw):
            setattr(obj, self.user_field, receiver)
            obj.save()

class BatchSurgeon(NopSurgeon):
    '''
    Merges two users just like DefaultSurgeon does but without calling
    save on each instance.
    '''
    
    def merge(self, receiver, donor):
        if receiver is donor:
            return
        donor.is_active = False
        donor.save()
        
        filter_kwargs = {'{0}'.format(self.user_field): donor}
        update_kwargs = {'{0}'.format(self.user_field): receiver}
        
        self.manager.filter(**filter_kwargs).update(**update_kwargs)
    
    