#!/usr/bin/env python
from setuptools import setup

version = '2.0.0'

setup(
    name='django-cache-utils',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['cache_utils'],

    url='https://github.com/adamghill/django-cache-utils',
    download_url='https://github.com/adamghill/django-cache-utils/archive/master.zip',
    license='MIT license',
    description="Caching decorator and django cache backend with advanced invalidation ability and dog-pile effect prevention",
    long_description=open('README.md').read(),
    install_requires = ['Django>=1.8,<1.9c', 'python-memcached'],
    test_suite="test_project.runtests.runtests",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
