#!/usr/bin/env python3
import unittest
import os
import sys
from contextlib import redirect_stdout
import filecmp
from collections import Counter

from count_files.utils.viewing_modes import show_2columns, show_result_for_search_files, \
    show_start_message, show_help_columns
from count_files.platforms import get_current_os


class TestViewingModes(unittest.TestCase):
    """Testing viewing_modes.py functions"""

    def setUp(self):
        self.test_file_total = self.get_locations('compare_tables', 'test_show_result_total.txt')
        self.test_file = self.get_locations('compare_tables', 'test_show_result_list.txt')
        if sys.platform.startswith('win'):
            self.standard_file = self.get_locations('compare_tables', 'win_show_result_list.txt')
        elif sys.platform.startswith('linux') or sys.platform.startswith('haiku'):
            self.standard_file = self.get_locations('compare_tables', 'linux_show_result_list.txt')
        elif sys.platform.startswith('darwin') or sys.platform.startswith('ios'):
            self.standard_file = self.get_locations('compare_tables', 'darwin_show_result_list.txt')
        self.current_os = get_current_os()

    def get_locations(self, *args):
        return os.path.normpath(os.path.join(os.path.dirname(__file__), *args))

    def generate_standard_file(self):
        with open(self.standard_file, 'w') as f:
            f.write(f"{self.get_locations('data_for_tests', 'no_extension')} (49.0 B)\n")
            f.write(f"{self.get_locations('data_for_tests', 'django_staticfiles_for_test', 'no_ext')} (0.0 B)\n")
            f.write('\n')
            f.write('   Found 2 file(s).\n')
            f.write('   Total combined size: 49.0 B.\n')
            f.write('   Average file size: 24.0 B (max: 49.0 B, min: 0.0 B).\n\n')
        return

    def write_to_test_file(self, filename, func, **kwargs):
        with open(filename, 'w') as f:
            with redirect_stdout(f):
                func(**kwargs)

    def test_show_2columns_usual(self):
        """Testing def show_2columns(compare files with tables).

        Comparison of the file with the results of the function with the specified file.
        standard: 2columns_sorted.txt and 2columns_most_common.txt
        results of the function: test_2columns_sorted.txt and test_2columns_most_common.txt
        :return:
        """
        test1 = self.get_locations('compare_tables', 'test_2columns_sorted.txt')
        test2 = self.get_locations('compare_tables', 'test_2columns_most_common.txt')

        usual_ext = Counter({'TXT': 3, 'GZ': 3, 'MD': 2, '[no extension]': 2, 'PY': 2,
                             'HTML': 1, 'JSON': 1, 'CSS': 1, 'WOFF': 1})

        usual_max_word_width = max(map(len, usual_ext.keys()))
        usual_total_occurrences = sum(usual_ext.values())

        usual_keys_sorted = {'data': sorted(usual_ext.items()), 'max_word_width': usual_max_word_width,
                             'total_occurrences': usual_total_occurrences,
                             'term_width': 80}
        usual_keys_common = {'data': usual_ext.most_common(), 'max_word_width': usual_max_word_width,
                             'total_occurrences': usual_total_occurrences,
                             'term_width': 100}

        self.write_to_test_file(test1, show_2columns, **usual_keys_sorted)
        self.write_to_test_file(test2, show_2columns, **usual_keys_common)

        self.assertEqual(filecmp.cmp(test1, self.get_locations('compare_tables', '2columns_sorted.txt'),
                                     shallow=False), True)
        self.assertEqual(filecmp.cmp(test2, self.get_locations('compare_tables', '2columns_most_common.txt'),
                                     shallow=False), True)

    def test_show_2columns_long(self):
        """Testing def show_2columns(compare files with tables).

        Comparison of the file with the results of the function with the specified file.
        standard: 2columns_sorted_long.txt and 2columns_most_common_long.txt
        results of the function: test_2columns_sorted_long.txt and test_2columns_most_common_long.txt
        :return:
        """
        test3 = self.get_locations('compare_tables', 'test_2columns_sorted_long.txt')
        test4 = self.get_locations('compare_tables', 'test_2columns_most_common_long.txt')

        # max ext len = 92
        long_ext = Counter({'MD': 2, 'PY': 2, 'HTML': 1, '0674532431': 1,
                            'INCREDIBLE_LONG_FILE_EXTENSION_INCREDIBLE_LONG_FILE_EXTENSION_'
                            'INCREDIBLE_LONG_FILE_EXTENSION': 1,
                            'MP3': 1, '7Z': 1})

        long_max_word_width = max(map(len, long_ext.keys()))
        long_total_occurrences = sum(long_ext.values())

        long_keys_sorted = {'data': sorted(long_ext.items()), 'max_word_width': long_max_word_width,
                            'total_occurrences': long_total_occurrences,
                            'term_width': 50}
        long_keys_common = {'data': long_ext.most_common(), 'max_word_width': long_max_word_width,
                            'total_occurrences': long_total_occurrences,
                            'term_width': 100}

        self.write_to_test_file(test3, show_2columns, **long_keys_sorted)
        self.write_to_test_file(test4, show_2columns, **long_keys_common)

        self.assertEqual(filecmp.cmp(test3, self.get_locations('compare_tables', '2columns_sorted_long.txt'),
                                     shallow=False), True)
        self.assertEqual(filecmp.cmp(test4, self.get_locations('compare_tables', '2columns_most_common_long.txt'),
                                     shallow=False), True)

    # TODO:  test show_result_for_search_files() for different OS
    # compare lists with paths and file sizes
    def test_show_result_for_search_files(self):
        """Testing def show_result_for_search_files. Search by extension.

        Comparison of the file with the results of the function with the specified file.
        Note: for different OS and PC lists will be different!
        Preconditions: create standard file for a particular PC
        Expected behavior: List with paths and file sizes.

        full/path/to/file1.extension (... KiB)
        full/path/to/file2.extension (... KiB)
        ...
        Found ... file(s).
        Total combined size: ... KiB.
        Average file size: ... KiB (max: ... KiB, min: ... B).
        :return:
        """
        self.generate_standard_file()
        print('A standard file is generated.')
        data = self.current_os.search_files(dirpath=self.get_locations('data_for_tests'), extension='.',
                                            include_hidden=False, recursive=True, case_sensitive=False)
        params = {'files': data, 'file_sizes': True}
        self.write_to_test_file(self.test_file, show_result_for_search_files, **params)
        self.assertEqual(filecmp.cmp(self.test_file, self.standard_file,
                                     shallow=False), True)

    def test_show_start_message(self):
        """Testing def show_start_message. Count, search, total group.

        :return:
        """
        count = show_start_message(value=None, case_sensitive=False, recursive=True, include_hidden=False,
                                   dirpath='/some/path', group=None)
        search = show_start_message(value='.', case_sensitive=False, recursive=False, include_hidden=False,
                                    dirpath='/some/path', group=None)
        total = show_start_message(value='TXT', case_sensitive=True, recursive=True, include_hidden=True,
                                   dirpath='/some/path', group='total')
        find = show_start_message(value='..', case_sensitive=True, recursive=True, include_hidden=True,
                                  dirpath='/some/path', group='find', contains=['abc', 'path', 'contains'])
        find1 = show_start_message(value='..', case_sensitive=False, recursive=False, include_hidden=False,
                                   dirpath='/some/path', group='find', contains=['def', 'filename', 'endswith'])
        self.assertEqual(count, 'Recursively counting all files, '
                                'ignoring hidden files and directories, in /some/path')
        self.assertEqual(search, 'Searching files without any extension, '
                                 'ignoring hidden files and directories, in /some/path')
        self.assertEqual(total, 'Recursively counting total number of files with (case-sensitive) extension .TXT, '
                                'including hidden files and directories, in /some/path')
        self.assertEqual(find, 'Recursively searching for paths that contain the substring "abc" '
                               '(case-sensitive), including hidden files and directories, in /some/path')
        self.assertEqual(find1, 'Searching for filenames that ends with the substring "def" '
                                '(case-insensitive), ignoring hidden files and directories, in /some/path')

    def test_show_help_columns(self):
        arguments = ['12345', '12345', '12345', '12345']
        list_result = show_help_columns(column_version=arguments, list_version=arguments,
                                        num_columns=2, term_width=10)
        table_result = show_help_columns(column_version=arguments, list_version=arguments,
                                         num_columns=2, term_width=50)
        self.assertEqual(list_result, '12345, 12345, 12345, 12345')
        self.assertEqual(table_result, ' 12345   12345   \n 12345   12345   \n ')

# from root directory:
# run all tests in test_viewing_modes.py
# python -m unittest tests/test_viewing_modes.py
# run all tests for class TestViewingModes
# python -m unittest tests.test_viewing_modes.TestViewingModes
# run test for def test_show_2columns in class TestViewingModes
# python -m unittest tests.test_word_counter.TestViewingModes.test_show_2columns

# or run file in PyCharm


if __name__ == '__main__':
    unittest.main()
