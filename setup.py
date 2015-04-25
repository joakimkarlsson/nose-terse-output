from setuptools import setup

setup(
    name='nose-terse-output',
    py_modules='terseout',

    install_requires=[
        'nose>=1.3.6'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'terseout = terseout:TerseOutPlugin'
        ]
    }
)
