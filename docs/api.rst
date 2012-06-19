=======================
django-transplant's API
=======================

Django-transplant attempts to split logic that performs User account merges
into atomic chunks that can be easily and separately maintained. ``Surgery``
and ``Surgeon`` classes perform these tasks.

-------------
Surgery class
-------------

``Surgery`` class' constructor accepts two string arguments::

  def __init__(self, model, surgeon):
      ...

It tries to instantiate instances of provided classes dynamically and it
will raise appropriate errors if this is impossible. Django-transplant's
bundled ``Surgery`` class accepts positional argumetn ``manager`` which
is a string representing manager that will be provided to ``Surgeon``.
Example use case is::

  my_surgery = Surgery(
    'myapp.models.Message',
    'myapp.models.DefaultSurgeon',
    manager='sent',
  )

This will create a surgery that will grab ``Message`` class, get its ``sent``
manager and provide it to ``DefaultSurgeon`` instance.

``Surgeon`` also provides a ``merge(receiver, donor)`` method that just calls
``Surgeon`` instance's ``merge``. The ``receiver`` should be the instance of
User that requests the merge, ``donor`` is the User that should be 'merged
into' receiver.

In your views you will probably want to use Surgery classes like this::

  # build a list of surgeries
  surgeries = []
  surgeries.append(Surgery(...))
  ...
  # perform merge using each surgery object
  for surgery in surgeries:
      surgery.merge(self.request.user, some_other_user)

-------------
Surgeon class
-------------

Django-transplant provides three generic ``Surgeon`` classes. They reside in
``transplant.surgeons`` module. Each of them implements a single ``merge``
method which takes two arguments - *receiver* and *donor* User instances.
This method accepts a keyword argument ``user_field`` which should be used
on provided model to change the field that will be updated during the merge.

``NopSurgeon``
  This ``Surgeon`` just sets up ``self.manager`` and ``self.user_field`` with
  an instance of ``Manager`` and a ``string`` respectively. It's merge method
  does nothing, but you are encouraged to subclass ``NopSurgeon`` if writing
  new ``Surgeon`` classes.

``DefaultSurgeon``
  Subclass of ``NopSurgeon``. Its merge method will:
    - set ``donor.is_active`` to false and donor will be saved.
    - get all objects from provided ``Manager`` and set their field provided
      by 'user_field' to ``receiver``.
    - will call save on all objects from manager, so that all signals are
      triggered.

``BatchSurgeon``
  Works exactly like ``DefaultSurgeon`` but won't call save methods. No signals
  will be triggered.

-------------------------
Extending django-template
-------------------------

Writing new subclasses of ``Surgeon`` and ``Surgery`` is easy.

While subclassing or writing new ``Surgery`` classes pleas  follow the
convention that ``__init__`` takes positional argument ``manager`` that
is provided later on to ``Surgeon`` to keep consistennt with
django-transplant's core.

While subclassing ``Surgeon`` classes override ``merge`` following the
convention to accept ``user_field``.
