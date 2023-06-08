import sys
from setuptools import setup, find_packages

requires = [
    'requests',
    'bs4'
]

setup(
    name='simple-search',
    description=("Basic and simple Python search application."),
    version='1.1',
    install_requires=requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['simple_search=simple_search.search:main'],
    },
    long_description=open('README.md').read(),
    keywords=['search', 'google', 'duckduckgo']
)
