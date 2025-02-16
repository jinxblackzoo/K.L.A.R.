#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
K.L.A.R. - Karteikarten Lernen Aber Richtig
Copyright (C) 2025 jinx@blackzoo.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from setuptools import setup, find_packages

setup(
    name='klar',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygobject',
        'reportlab',
        'sqlalchemy'
    ],
    entry_points={
        'console_scripts': [
            'klar=klar.main:main'
        ]
    },
    author="jinx@blackzoo.de",
    author_email="jinx@blackzoo.de",
    description="K.L.A.R. - Karteikarten Lernen Aber Richtig",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="education, learning, flashcards, gtk4",
    url="https://github.com/jinxblackzoo/K.L.A.R.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
    python_requires='>=3.8',
    license="GNU General Public License v3 (GPLv3)",
)
