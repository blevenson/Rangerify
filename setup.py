"""
Music streaming server python package configuration.

Brett Levenson  <brettlev@umich.edu>
"""

from setuptools import setup

setup(
    name='music',
    version='0.1.0',
    packages=['music'],
    include_package_data=True,
    install_requires=[
        'flask==0.12.2',
        'arrow==0.10.0',
        'html5validator==0.2.8',
        'pycodestyle==2.3.1',
        'pydocstyle==2.0.0',
        'Flask-Testing==0.6.2',
        'selenium==3.6.0',
        'pylint==2.1.1',
        'requests==2.18.4',
        'sh==1.12.14',
    ],
)
