#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the MoCo project
#
# Copyright (c) 2020 ALBA controls team
# Distributed under the GNU General Public License v3.
# See LICENSE for more info.

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    "pyserial>=3.5",
]

extra_requirements = {
    "tango": ["pytango"],
    "simulator": ["sinstruments>=1"],
    "sardana": ["sardana>=3.0.3", 'click']
}
if extra_requirements:
    extra_requirements["all"] = list(set.union(*(set(i) for i in
                                                 extra_requirements.values())))

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="ALBA controls team",
    author_email='controls@cells.es',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Library, simulator, Tango server and Sardana plugins for "
                "Monochromator Controller MoCo",
    entry_points={
        'console_scripts': [
            'Moco=moco.tango.server.__main__:main [tango]',
        ],
    },
    extras_require=extra_requirements,
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n',
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='moco',
    name='moco',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ALBA-Synchrotron/MoCo',
    version='2.0.0',
    zip_safe=False,
)




