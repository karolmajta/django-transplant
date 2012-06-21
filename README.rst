=================
django-transplant
=================

--------
Overview
--------

Django-transplant is an app for performing easy merges of django user
accounts. It should play nicely with any third party social authentication
backend.

------------
Requirements
------------

Django-transplant requires:

- Django 1.2.5 or higher.

If you plan to develop, or run the test suite you should also install:

- Mock
 
This dependency **will not** be installed automatically via pip.

----------
Installing
----------

To install with pip into site-packages issue::

	pip install django-transplant

To install with pip into src folder (as git repo) issue::

	pip install -e \
	git+http://github.com/lolek09/django-transplant#egg=django-transplant

-------------
Configuration
-------------

Add ``'transplant'`` to your ``INSTALLED_APPS``. If you plan to run the test
suite you should also add ``'transplant.tests'``::

	INSTALLED_APPS += (
		'transplant',
		'transplant.tests', # this is optional
	)

For your convenience django-transplant provides a default view for performing
User merges. You can use it like any FormView, and it's name is
``transplant_merge``. It expects a default template in 'transplant/merge.html'.

To hook it up just add it to your ``urlconf`` at any URL::

	urplatterns = patterns('',
		...
		url(r'^accounts/merge/$', include('transplant.urls')),
		...
	)

You should be now able to get the merge form and submit it, but it will have
no effect. To utilize default merges you must set ``TRANSPLANT_OPERATIONS``
in your settings.py::

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

- set field given as 'user_field' to the user that performs the merge
- call save() on each entity (so that all signals are triggered)
- set the is_active to False on the user that is merged

If you want additional functionality consult the docs.

-------------
Documentation
-------------

Documentation is available at
`http://django-transplant.readthedocs.org/ <http://django-transplant.readthedocs.org/>`_

---------
Changelog
---------

-----
0.0.2
-----

  - Addidional Surgeon class BatchSurgeon pefrorming batch updates
  - Added UserMergeForm used by default by provided view

-----
0.0.1
-----

  - Surgery class
  - Surgeon classes
    - NopSurgeon class that does basically nothing
    - DefaultSurgeon class for default merging behavior
  - Default view provide for convenience
  - Urls provided for conveniene
