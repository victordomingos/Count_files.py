#!/usr/bin/env python3
import unittest
import os
import sys

from count_files.__main__ import main_flow


class TestArgumentParser(unittest.TestCase):
    """Testing a parser with different arguments"""

    def get_locations(self, *args):
        return os.path.normpath(os.path.join(os.path.dirname(__file__), *args))

    # searching by pattern with include_hidden=True(suitable for all operation systems), found group
    def test_path_contains_argument(self):
        self.assertEqual(main_flow([self.get_locations(), '-pc', 'os_file', '-a']), 1)
        self.assertEqual(main_flow([self.get_locations(), '-pc', '2columns', '-a']), 8)
        self.assertEqual(main_flow([self.get_locations(), '-pc', 'cprofile_test.py', '-a']), 1)
        # little faster than -fe, but less accurate
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-pc', '.TXT', '-c', '-a']), 1)

    def test_extension_contains_argument(self):
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-ec', '*j*', '-a']), 1)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-ec', '*X*', '-a', '-c']), 1)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-ec', 'm*', '-a']), 2)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-ec', '*tml', '-a']), 1)

    def test_filename_contains_argument(self):
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-fc', '*no_extension*', '-a']), 1)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-fc', '*_ext', '-a']), 1)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-fc', '*_EXT', '-a', '-c']), 0)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-fc', 'ext_*', '-a']), 2)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-fc', 'html_file', '-a']), 1)

    # counting total number of files
    def test_countfiles_all_t(self):
        """Testing def main_flow.

        Recursive/non recursive counting.
        Testing for hidden files is not carried out here.
        Equivalent to "count-files ~/.../tests/data_for_tests -a -t .."
        :return:
        """
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-t', '..']), 16)
        self.assertEqual(main_flow([self.get_locations('data_for_tests'), '-t', '..', '-nr']), 6)

    # search by extension
    def test_countfiles_fe(self):
        """Testing def main_flow.

        Recursive default counting.
        Equivalent to
        "count-files ~/.../tests/data_for_tests/django_staticfiles_for_test -fe {extension}"
        Non recursive counting.
        Equivalent to
        "count-files ~/.../tests/data_for_tests/django_staticfiles_for_test -nr -fe {extension}"
        :return:
        """
        location = self.get_locations('data_for_tests')
        extensions = {'py': 2, 'json': 1, 'woff': 1, '.': 2, 'TXT': 3, 'txt': 3}
        nr_extensions = {'css': 0, '.': 1, 'TXT': 1, 'txt': 1}
        # case-insensitive and recursive
        for k, v in extensions.items():
            with self.subTest(k=k, v=v):
                self.assertEqual(main_flow([location, '-fe', f'{k}']), v)
        # case-sensitive and non-recursive
        for k, v in nr_extensions.items():
            with self.subTest(k=k, v=v):
                self.assertEqual(main_flow([location, '-nr', '-c', '-fe', f'{k}']), v)

    # tests for hidden files, Linux and Mac OS
    @unittest.skipIf(sys.platform.startswith("win"), "not for Windows")
    def test_for_hidden(self):
        """Testing def main_flow.

        Equivalent to
        "python __main__.py ~/.../tests/data_for_tests -nr -t .."
        and "python __main__.py ~/.../tests/data_for_tests -nr -a -t .."
        :return:
        """
        self.assertEqual(main_flow([self.get_locations('test_hidden_linux'), '-nr', '-t', '..']), 1)
        self.assertEqual(main_flow([self.get_locations('test_hidden_linux'), '-nr', '-t', '..', '-a']), 2)

    # tests for hidden files, Windows
    @unittest.skipUnless(sys.platform.startswith('win'), 'for Windows')
    def test_for_hidden_win(self):
        """Testing def main_flow.

        Equivalent to
        "python __main__.py ~/.../tests/data_for_tests -nr -t .."
        and "python __main__.py ~/.../tests/data_for_tests -nr -a -t .."
        :return:
        """
        self.assertEqual(main_flow([self.get_locations('test_hidden_windows'), '-nr', '-t', '..']), 1)
        self.assertEqual(main_flow([self.get_locations('test_hidden_windows'), '-nr', '-t', '..', '-a']), 2)

# from root directory:

# run all tests in test_argument_parser.py
# python -m unittest tests/test_argument_parser.py

# run all tests for class TestArgumentParser
# python -m unittest tests.test_argument_parser.TestArgumentParser

# run test for def test_for_hidden in class TestArgumentParser
# python -m unittest tests.test_argument_parser.TestArgumentParser.test_for_hidden

# or run file in PyCharm


if __name__ == '__main__':
    unittest.main()
