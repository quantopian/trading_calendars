#!/usr/bin/env python
#
# Copyright 2018 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import (
    find_packages,
    setup,
)

import versioneer

DISTNAME = "trading_calendars"
DESCRIPTION = """trading_calendars is a Python library with \
securities exchange calendars used by Quantopian's Zipline."""

AUTHOR = "Quantopian Inc"
AUTHOR_EMAIL = "opensource@quantopian.com"
URL = "https://github.com/quantopian/trading_calendars"
LICENSE = "Apache License, Version 2.0"

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: Apache Software License",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Operating System :: OS Independent"
]

reqs = [
    "numpy",
    "pandas",
    "pytz",
    "toolz",
]

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

if __name__ == '__main__':
    setup(
        name=DISTNAME,
        entry_points={
            'console_scripts': [
                'tcal = trading_calendars.tcal:main',
            ],
        },
        cmdclass=versioneer.get_cmdclass(),
        version=versioneer.get_version(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        classifiers=classifiers,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(
            include=['trading_calendars', 'trading_calendars.*']
        ),
        install_requires=reqs,
    )
