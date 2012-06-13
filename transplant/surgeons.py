'''
This module contains Surgeon classes. Surgeon objects perform operation on
models' querysets and user instances when performing an account merge.
'''

class NopSurgeon:
    '''
    This is a surgeon class that performs a 'merge' by doing nothing
    (it leaves the database unchanged).
    '''
    def __init__(self, queryset, user_field='user'):
        self.user_field = user_field
        self.queryset = queryset

    def merge(self, receiver, donor):
        '''
        Merges two users. In this implementation this method does nothing.
        '''
        pass

class DefaultSurgeon(NopSurgeon):
    '''
    This class merges two users by setting user (or a field given as
    'user_field') to receiver on all objects in given queryset and calling
    save() on each of them (so that all signals etc. are fired)
    '''
    
    def merge(self, receiver, donor):
        '''
        Sets donor.is_active to false,
        '''
        donor.is_active = False
        donor.save()
        
        for obj in self.queryset.all():
            setattr(obj, self.user_field, receiver)
            obj.save()