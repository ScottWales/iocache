#!/usr/bin/env python
"""
Copyright 2015 Scott Wales

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
import pytest

from scache.Cache import Cache, trace_re

@pytest.fixture(scope='session')
def cache(tmpdir_factory):
    cache_path = tmpdir_factory.mktemp('cache').strpath
    return Cache(cache_path = cache_path)

def test_parse_trace(tmpdir, cache):
    a = tmpdir.join('a')
    a.write('a')
    a_path = a.strpath

    b = tmpdir.join('b')
    b.write('b')
    b_path = b.strpath
    
    cache.parse_trace('open("%s", O_RDONLY) = 1'%a_path)
    cache.parse_trace('open("%s", O_WRONLY) = 2'%b_path)
