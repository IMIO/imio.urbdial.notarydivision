# -*- coding: utf-8 -*-
"""Installer for the imio.urbdial.notarydivision package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='imio.urbdial.notarydivision',
    version='0.1',
    description="",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Zope Plone',
    author='Franck NGAHA',
    author_email='franck.o.ngaha@gmail.com',
    url='http://pypi.python.org/pypi/imio.urbdial.notarydivision',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['imio', 'imio.urbdial'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.ckeditor',
        'collective.js.jqueryui',
        'collective.z3cform.datagridfield',
        'collective.z3cform.rolefield',
        'imio.actionspanel',
        'imio.helpers',
        'plone.api',
        'plone.directives.dexterity',
        'plone.formwidget.masterselect',
        'plone.formwidget.multifile',
        'setuptools',
        'z3c.table',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
