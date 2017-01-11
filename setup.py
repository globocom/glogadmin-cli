#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pip==8.1.2',
    'bumpversion==0.5.3',
    'wheel==0.29.0',
    'watchdog==0.8.3',
    'flake8==2.6.0',
    'tox==2.3.1',
    'coverage==4.1',
    'glogcli==0.8.2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='glogadmincli',
    version='0.1.0',
    description="Graylog admin command line interface.",
    long_description=readme + '\n\n' + history,
    author="Sinval Vieira Mendes Neto",
    author_email='sinvalneto01@gmail.com',
    url='https://github.com/sinvalmendes/glogadmin-cli',
    packages=[
        'glogadmincli',
    ],
    package_dir={'glogadmincli':
                 'glogadmincli'},
    entry_points={
        'console_scripts': [
            'glogadmincli=glogadmincli.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='glogadmin-cli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
