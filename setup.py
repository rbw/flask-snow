# -*- coding: utf-8 -*-

"""
flask-snow
------------

Adds ServiceNow support to Flask applications with the help of the `pysnow`_ library.

"""

import io
import ast

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    """ Parses main module and fetches version attribute from the syntax tree

    :return: flask-snow version

    """
    with io.open('flask_snow/__init__.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with io.open('README.rst') as readme:
    setup(
        name='flask-snow',
        version=get_version(),
        url='https://github.com/rbw0/flask-snow',
        license='MIT',
        author='Robert Wikman',
        author_email='rbw@vault13.org',
        maintainer='Robert Wikman',
        maintainer_email='rbw@vault13.org',
        description='Pysnow extension for Flask',
        download_url='https://github.com/rbw0/flask-snow/tarball/%s' % get_version(),
        long_description=readme.read(),
        packages=['flask_snow'],
        zip_safe=False,
        include_package_data=True,
        platforms='any',
        install_requires=[
            'Flask',
            'Flask-Sphinx-Themes',
            'pysnow',
            'requests'
        ],
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
