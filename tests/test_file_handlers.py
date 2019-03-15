import unittest
import os

from count_files.utils.file_handlers import get_file_extension, get_pattern_substring_and_type, \
    check_pattern_matching


class TestFileHandlers(unittest.TestCase):

    def get_locations(self, *args):
        return os.path.normpath(os.path.join(os.path.dirname(__file__), *args))

    def test_get_file_extension(self):
        """Testing def get_file_extension.

        Extract only the file extension from a given path.
        Expected behavior: return extension name (txt, py) or '.' (for files without extension)
        :return:
        """
        extensions_dict = {'file.py': 'py', '.gitignore': '.', 'image.JPG': 'JPG',
                           'file': '.', '.hidden_file.txt': 'txt',
                           '.hidden.file.txt': 'txt', 'select2.3805311d5fc1.css.gz': 'gz'
                           }
        for k, v in extensions_dict.items():
            with self.subTest(k=k, v=v):
                self.assertEqual(get_file_extension(k, case_sensitive=True), v)

    def test_get_pattern_substring_and_type(self):
        ext_dict = {'substring*': ('startswith', 'substring'), '*substring': ('endswith', 'substring'),
                    '*substring*': ('contains', 'substring'), 'substring': ('contains', 'substring'),
                    '*': ('startswith', '*'), '**': ('endswith', '*'),
                    '***': ('contains', '*'), '****': ('contains', '**'),
                    'sub?str.ing': ('contains', 'sub?str.ing'), '**substring': ('endswith', '*substring'),
                    'substring***': ('startswith', 'substring**'), '**substring*': ('contains', '*substring')}
        for k, v in ext_dict.items():
            with self.subTest(k=k, v=v):
                self.assertEqual(get_pattern_substring_and_type(k), v)

    def test_check_pattern_matching(self):
        """
        param extension_pattern cleared in def get_extension_pattern_and_type
        :return:
        """
        # file_name, file_path,
        # pattern_type, substring, case, where, result
        test_list = [('py_file_for_tests.py', self.get_locations('data_for_tests', 'py_file_for_tests.py'),
                      'contains', 'for', False, 'filename', True),
                     ('py_file_for_tests.py', self.get_locations('data_for_tests', 'py_file_for_tests.py'),
                      'contains', 'django', False, 'path', False),
                     ('py_file_for_tests.py', self.get_locations('data_for_tests', 'py_file_for_tests.py'),
                     'startswith', 'py', False, 'extension', True),
                     ('ext_in_uppercase.TXT', self.get_locations('data_for_tests', 'ext_in_uppercase.TXT'),
                     'endswith', 'T', True, 'extension', True),
                     # default False for [no_extension]
                     ('no_extension', self.get_locations('data_for_tests', 'no_extension'),
                      'contains', 'n', False, 'extension', False),
                     ]
        for i in test_list:
            with self.subTest(i=i):
                self.assertEqual(check_pattern_matching(file_name=i[0], file_path=i[1], pattern_type=i[2],
                                                        substring=i[3], case_sensitive=i[4], where=i[5]), i[6])


if __name__ == '__main__':
    unittest.main()
