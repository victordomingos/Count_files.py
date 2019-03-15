import unittest
import os

from count_files.platforms import get_current_os


class TestFindPatterns(unittest.TestCase):

    def setUp(self):
        self.current_os = get_current_os()

    def get_locations(self, *args):
        return os.path.normpath(os.path.join(os.path.dirname(__file__), *args))

    def test_find_group_pc(self):
        # get all matches count-files -pc substring
        # contains ['substring', 'where', 'type']
        result = self.current_os.search_files(self.get_locations('data_for_tests'),
                                              '..', contains=['django', 'path', 'contains'],
                                              recursive=True, include_hidden=True, case_sensitive=False)
        result1 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['ext', 'path', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result2 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['webfont', 'path', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result3 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['SELECT2', 'path', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=True)
        self.assertEqual(len(list(result)), 10)
        self.assertEqual(len(list(result1)), 4)
        self.assertEqual(len(list(result2)), 1)
        self.assertEqual(len(list(result3)), 2)

    def test_find_group_pc2(self):
        # get all matches count-files -pc substring
        result = self.current_os.search_files(self.get_locations('data_for_tests'),
                                              '..', contains=[f'css{os.sep}vendor', 'path', 'contains'],
                                              recursive=True, include_hidden=True, case_sensitive=False)
        result1 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['staticfiles.json', 'path', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result2 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['.txt.gz', 'path', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        self.assertEqual(len(list(result)), 4)
        self.assertEqual(len(list(result1)), 1)
        self.assertEqual(len(list(result2)), 1)

    def test_find_group_ec(self):
        result = self.current_os.search_files(self.get_locations('data_for_tests'),
                                              '..', contains=['htm', 'extension', 'startswith'],
                                              recursive=True, include_hidden=True, case_sensitive=False)
        result1 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['on', 'extension', 'endswith'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result2 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['md', 'extension', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result3 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['T', 'extension', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=True)
        self.assertEqual(len(list(result)), 1)
        self.assertEqual(len(list(result1)), 1)
        self.assertEqual(len(list(result2)), 2)
        self.assertEqual(len(list(result3)), 1)

    def test_find_group_fc(self):
        result = self.current_os.search_files(self.get_locations('data_for_tests'),
                                              '..', contains=['html', 'filename', 'startswith'],
                                              recursive=True, include_hidden=True, case_sensitive=False)
        result1 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['on', 'filename', 'endswith'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result2 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['ext', 'filename', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=False)
        result3 = self.current_os.search_files(self.get_locations('data_for_tests'),
                                               '..', contains=['LICENSE', 'filename', 'contains'],
                                               recursive=True, include_hidden=True, case_sensitive=True)
        self.assertEqual(len(list(result)), 1)
        self.assertEqual(len(list(result1)), 1)
        self.assertEqual(len(list(result2)), 4)
        self.assertEqual(len(list(result3)), 4)

# python -m unittest tests.test_find_with_patterns.TestFindPatterns
# python -m unittest tests.test_find_with_patterns.TestFindPatterns.test_find_group_fc


if __name__ == '__main__':
    unittest.main()
