'''
Setup file for easy installation
'''
from os.path import join, dirname
from setuptools import setup

LONG_DESCRIPTION = '''
django-transplant is a tool for performing easy automated merges of
user accounts.

It should play nicely with any third party auth backend.
'''


def long_description():
    '''
    Return long description from README.rst if it's present
    because it doesn't get installed.
    '''
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION

setup(name='django-transplant',
      version='0.0.1',
      author='Karol Majta',
      author_email='karolmajta@gmail.com',
      description='Automated merges of User accounts.',
      license='BSD',
      keywords='django, user, account, merge',
      url='https://github.com/lolek09/django-transplant',
      packages=['transplant',
                'transplant.tests'],
      package_data={'social_auth':['locale/*/LC_MESSAGES/*']},
      long_description=long_description(),
      install_requires=['django>=1.2.5'],
      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.7'])