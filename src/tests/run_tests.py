#!/usr/bin/env python

import os
import sys
import unittest

IGNORE_FILES = ['run_tests.py',]

suite = unittest.TestSuite()
debug = True

try:
    descriptions = sys.argv[1]
    verbosity = sys.argv[1]
except IndexError:
    descriptions = 2
    verbosity = 2

try:
    if sys.argv[2] == '1':
        debug = True
except IndexError:
    pass

for file in os.listdir(os.path.abspath('.')):
    if file in IGNORE_FILES:
        continue
    if file[-3:] != '.py':
        continue
    if debug: 
        print 'Found test : %s' % file[:-3]
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(file[:-3]))

test_runner = unittest.TextTestRunner(descriptions=descriptions, verbosity=verbosity)
result = test_runner.run(suite)
if result.failures or result.errors:
    sys.exit(1)

