============
Configuration
============

--------------------------
Configuring INSTALLED_APPS
--------------------------

Add 'transplant' to your ``INSTALLED_APPS``. If you plan to run the test suite
you should also add 'transplant.tests'::

  INSTALLED_APPS += (
		'transplant',
		'transplant.tests', # this is optional
	)

-----------------------
Hooking up default URLs
-----------------------

For your convenience django-transplant provides a default view for performing
User merges. You can use it like any FormView, and it's name is
``transplant_merge``. It expects a default template in 'transplant/merge.html'.

To hook it up just add it to your ``urlconf`` at any URL::

	urplatterns = patterns('',
		...
		url(r'^accounts/merge/$', include('transplant.urls')),
		...
	)

-------------------------------
Hooking up view in your urls.py
-------------------------------

``transplant.views.TransplantMergeView`` is a subclass of generic ``FormView``
so you can hook it directly to your urls. You can pass it's arguments like you
would to any other generic view::

  ...
  from django.contrib.auth.decorators import login_required
  
  from views import TransplantMergeView
  ...
  
  urlpatterns = patterns('',
      ...
      url(r'^$',
          login_required(TransplantMergeView.as_view(
              template_name='custom/template/name.html')
          ),
          name='custom_name'
      ),
      ...
  )

----------------------------------------------------
Configuring TRANSPLAN_OPERATIONS in your settings.py
----------------------------------------------------

After setting URLs yous should be able to get the merge form and submit it,
but it will have no effect. To utilize default merges you must set
``TRANSPLANT_OPERATIONS`` in your settings.py::

	TRANSPLANT_OPERATIONS = (
	    (
	    	'transplant.tests.models.CustomProfile',
	    	'transplant.surgeons.DefaultSurgeon',
	    	{}
	    ),
	    (
	        'transplant.tests.models.Item',
	        'transplant.tests.surgeons.DefaultSurgeon',
	        {'user_field': 'owner'}
	    ),
	    (
	        'transplant.tests.models.Message',
	        'transplant.tests.surgeons.DefaultSurgeon',
	        {'manager': 'unread'}
	    ),
	)

``TRANSPLANT_OPERATIONS`` consists of triples, each one of them specifies:

1. Path to model class to be merged.
2. Path to ``Surgeon`` class to be used during the merge.
3. Extra arguments.

Currently supported extra arguments are:

- ``user_field`` - name of the user field that will be used by the Surgeon
  during the merge (defaults to 'user').
- ``manager`` - name of Manager used during the merge. In the example above
  only messages accessible via the 'unread' manager will be merged.
  
You may be happy with the behavior of ``DefaultSurgeon`` which is:

- set field given as ``'user_field'`` to the user that performs the merge
- call ``save()`` on each entity (so that all signals are triggered)
- set the ``is_active`` to False on the user that is merged

If you want additional functionality consult API docs.