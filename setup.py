import sys
from setuptools import setup, find_packages

requires = [
    'bs4',
]

setup(
    name='basic_search',
    description=("Basic and simple Python search application."),
    version='1.0',
    install_requires=requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['basic-search=basic_search.search:main'],
    },
    #long_description=open('README.md').read(),
    keywords=['search', 'google', 'duckduckgo']
)
