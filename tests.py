#!/usr/bin/env python
# coding: utf-8

"""
    Test suite for the Pythonista Docker image
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Run the following command inside Pythonista container in order to
    check everything inside works as expected:

        $ python path/to/tests.py

    Please note that test cases MUST be changed each time the Python
    interpreter version is changed.

    :copyright: (c) 2015 Igor Kalnitsky
    :license: 3-clause BSD
"""

from __future__ import unicode_literals

import unittest
import subprocess


class TestPyVersions(unittest.TestCase):
    """
    Ensure that system has expected Python interpreters and proper defaults.

    Just run consequently supported Python interpreters, print their version
    and check that they are expected. Test fails if one of interpreters is
    missed or has unexpected minor version.
    """

    _py_ver = 'import sys; sys.stdout.write("%d.%d.%d" % sys.version_info[:3])'

    def _get_py_version(self, py_interpreter):
        stdout = subprocess.check_output(
            "{0} -c '{1}'".format(py_interpreter, self._py_ver),
            shell=True)
        return stdout.decode('ascii')

    def test_py26(self):
        self.assertEqual('2.6.9', self._get_py_version('python2.6'))

    def test_py27(self):
        self.assertEqual('2.7.10', self._get_py_version('python2.7'))

    def test_py32(self):
        self.assertEqual('3.2.6', self._get_py_version('python3.2'))

    def test_py33(self):
        self.assertEqual('3.3.6', self._get_py_version('python3.3'))

    def test_py34(self):
        self.assertEqual('3.4.3', self._get_py_version('python3.4'))

    def test_py35(self):
        self.assertEqual('3.5.0', self._get_py_version('python3.5'))

    def test_pypy(self):
        self.assertEqual('2.7.10', self._get_py_version('pypy'))

    def test_pypy3(self):
        self.assertEqual('3.2.5', self._get_py_version('pypy3'))

    def test_py2_default(self):
        self.assertEqual('2.7.10', self._get_py_version('python2'))

    def test_py3_default(self):
        self.assertEqual('3.5.0', self._get_py_version('python3'))


class _TestModuleSupport(unittest.TestCase):
    """
    A base class for testing module support in Python interpreters.

    In order to test that Python interpreter is built with some module
    support just inherit this class and override its properties.
    """

    py_code = None

    def _execute_code(self, py_interpreter):
        retcode = subprocess.call(
            "{0} -c '{1}'".format(py_interpreter, self.py_code),
            shell=True)
        return retcode

    def test_py26(self):
        self.assertEqual(0, self._execute_code('python2.6'))

    def test_py27(self):
        self.assertEqual(0, self._execute_code('python2.7'))

    def test_py32(self):
        self.assertEqual(0, self._execute_code('python3.2'))

    def test_py33(self):
        self.assertEqual(0, self._execute_code('python3.3'))

    def test_py34(self):
        self.assertEqual(0, self._execute_code('python3.4'))

    def test_py35(self):
        self.assertEqual(0, self._execute_code('python3.5'))

    def test_pypy(self):
        self.assertEqual(0, self._execute_code('pypy'))

    def test_pypy3(self):
        self.assertEqual(0, self._execute_code('pypy3'))


class TestSqlite3Support(_TestModuleSupport):
    """
    Check that Python interpreters are built with sqlite3 support.

    It requires to have libsqlite3-dev installed to build CPython with
    sqlite3 support.
    """

    py_code = 'import sqlite3'


class TestZlibSupport(_TestModuleSupport):
    """
    Check that Python interpreters are built with zlib1 support.

    It requires to have zlib1g-dev installed to build CPython with
    zlib/gzip support.
    """

    py_code = 'import gzip; import zlib'


if __name__ == '__main__':
    # we aren't interested in running tests of base test cases, so just
    # remove it from the scope since it's simplest that we can do
    del _TestModuleSupport
    unittest.main()
