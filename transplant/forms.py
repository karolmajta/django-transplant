'''
Currently contains just one form:
  - UserMergeForm
  It's basically an authentication form with an extra checkbox for warning
  confirmation.
'''
from django.forms import BooleanField
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import AuthenticationForm

class UserMergeForm(AuthenticationForm):
    '''
    Form for merging user accounts
    '''
    
    warning_accepted = BooleanField(
        label = _('I understand the warning.'),
    )