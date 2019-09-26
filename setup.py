#!/usr/bin/env python
"""
Packaging script to create source packages and wheels
"""

from setuptools import setup, find_packages

setup(
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
