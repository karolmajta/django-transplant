=====
About
=====

--------
Overview
--------

Django-transplant is an app for performing easy merges of django user accounts.
It should play nicely with any third party social authentication backend.

----------------------------------
Rationale behind django-transplant
----------------------------------

When using third party authentication apps for django it is common that users
create more than one account for themselves. While some apps provide ways to
easily attach social accounts so django's native user accounts, others don't.
This approach is often based on email addresses pulled from the authentication
services, and may sometimes fail (i.e. if no e-mail data is available).

Django-transplant enables quick merges of user accounts performed on demand.
Moreover it allows you to keep your logic on how to perform these merges away
from views. Django-transplant provides some basic classes to reduce your
boilerplate, and allow easy extensibility.