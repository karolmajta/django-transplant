from django.views.generic import FormView
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect

from forms import UserMergeForm
from surgery import Surgery

class TransplantMergeView(FormView):
    '''
    View performing User merge using all operations defined in
    settings.TRANSPLANT_OPERATIONS.
    
    Handles transactions (rollback on any exception) and exceptions
    (see transplant.settings for full info).
    
    Uses django.contrib.auth.forms.AuthenticationForm by default, but any
    other Form that will conform to it's API can do (the get_user() method!)
    '''
    form_class = UserMergeForm
    success_url = settings.TRANSPLANT_SUCCESS_URL
    template_name = 'transplant/merge.html'
    def __init__(self, **kwargs):
        FormView.__init__(self, **kwargs)
    
    def form_valid(self, form):
        receiver = self.request.user
        donor = form.get_user()
        operations = [o for o in settings.TRANSPLANT_OPERATIONS]
        with transaction.commit_manually():
            try:
                for operation in operations:
                    Surgery(operation[0], operation[1], **operation[2]).merge(receiver, donor)
                transaction.commit()
                return super(TransplantMergeView, self).form_valid(form)
            except Exception as e:
                transaction.rollback()
                return self.dispatch_exception(e)
        return super(TransplantMergeView, self).form_valid(form)
    
    def dispatch_exception(self, e):
        if settings.DEBUG is True:
            raise e
        else:
            if settings.TRANSPLANT_FAILURE_URL is None:
                raise e
            else:
                return HttpResponseRedirect(settings.TRANSPLANT_FAILURE_URL)
    
    def get_form_kwargs(self):
        form_kwargs = super(TransplantMergeView, self).get_form_kwargs()
        form_kwargs.update({'prefix': 'merge'})
        return form_kwargs
    
    def get_context_data(self, **kwargs):
        context_data = super(FormView, self).get_context_data(**kwargs)
        context_data.update({'merge_form': context_data['form']})
        return context_data