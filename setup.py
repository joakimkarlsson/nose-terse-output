#!/usr/bin/env python
from setuptools import setup

setup(
    name='nose-terse-output',
    version='1.0.0',
    description='Terse output from your nose tests',
    long_description=open('README.rst').read(),
    url='https://github.com/joakimkarlsson/nose-terse-output',
    author='Joakim Karlsson',
    author_email='joakim@jkarlsson.com',

    py_modules=['terseout'],

    install_requires=[
        'nose>=1.3.6'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'terseout = terseout:TerseOutPlugin'
        ]
    },

    keywords=['unit testing', 'nose']
)
