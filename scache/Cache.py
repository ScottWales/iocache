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

from __future__ import print_function

import re
import sys
import os
from subprocess import Popen, PIPE

from checksum import checksum

trace_re = re.compile('^(\[.*\] )?open\("(.*)", (.*)\) += (.*)$')

class Cache:
    def __init__(self, cache_path = None):
        """
        Set the Cache path
        """
        if cache_path is not None:
            self.cache_path = cache_path
        else:
            self.cache_path = os.path.join(os.environ['HOME'],'.scache')

        self.ignore_re = re.compile('^/(bin|dev|etc|lib|lib32|lib64|usr|opt|proc|var)')

    def recall(self, args):
        """
        Try to run a command, using the cached output if possible
        """
        self.remember(args)

    def remember(self, args):
        """
        Run a command and put it in the cache
        """
        trace    = ['strace', '-q','-f','-etrace=open','-esignal=!all']
        proc     = Popen(trace + args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()

        print(out, file=sys.stdout)
        self.parse_trace(err)

    def parse_trace(self, err):
        for line in err.splitlines():
            match = trace_re.match(line)
            if match is None:
                print(line, file=sys.stderr)
            else:
                self.parse_open(match)

    def parse_open(self, match):
        """
        Check a file open call to see if it succeeded and is not in the ignore
        list. Send reads and writes to `add_input()` and `add_output()`
        respectively.
        """
        filename = match.group(2)
        mode     = match.group(3)
        result   = match.group(4)

        code = int(result.split()[0])
        if code < 0:
            return
        if self.ignore_re.match(filename) is not None:
            return
        if 'O_RDONLY' in mode:
            self.add_input(filename)
        if 'O_WRONLY' in mode:
            self.add_output(filename)

    def add_input(self, filename):
        check = checksum(filename)
        print('input', filename, check)

    def add_output(self, filename):
        check = checksum(filename)
        cache_path = os.path.join(self.cache_path,check[0:6],check)
        print('output', filename, cache_path)
