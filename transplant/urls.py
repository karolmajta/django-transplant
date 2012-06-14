from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import TransplantMergeView

urlpatterns = patterns('',
    url(r'^$',
        login_required(TransplantMergeView.as_view()),
        name='transplant_merge'
    ),
)