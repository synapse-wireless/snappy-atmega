#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='snappyatmega',
    description="Advanced SNAPpy includes for Synapse SNAP modules based on the atmega128rfa1",
    maintainer='Tyler Crumpton',
    maintainer_email='tyler.crumpton@synapse-wireless.com',
    url='https://github.com/synapse-wireless/snappy-atmega',
    packages=['snappyatmega'],
    install_requires=['vcversioner'],
    vcversioner={
        'version_module_paths': ['snappyatmega/_version.py'],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ],
)
