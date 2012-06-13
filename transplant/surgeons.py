'''
This module contains Surgeon classes. Surgeon objects perform operation on
models' querysets and user instances when performing an account merge.
'''

class NopSurgeon:
    '''
    This is a surgeon class that performs a 'merge' by doing nothing
    (it leaves the database unchanged).
    '''
    def __init__(self, receiver, donor, model, user_field='user', queryset='objects'):
        self.model = model
        self.receiver = receiver
        self.donor = donor
        self.user_field = user_field
        self.queryset = queryset
        