#!/usr/bin/env python
"""
Copyright 2015 ARC Centre of Excellence for Climate Systems Science

author: Scott Wales <scott.wales@unimelb.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages
from scache.meta import __NAME__, __VERSION__, __AUTHOR__, __LICENSE__

setup(
        name         = __NAME__,
        version      = __VERSION__,
        author       = __AUTHOR__,
        author_email = 'scott.wales@unimelb.edu.au',
        license      = __LICENSE__,
        packages     = find_packages(__NAME__),
        entry_points = {
            'console_scripts': [
                'scache = scache.main:main',
                ]
            }
        )
