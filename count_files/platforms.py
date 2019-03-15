import os
import sys
from pathlib import Path
from typing import Iterable, List
from collections import Counter
try:
    import ctypes
except:
    pass

from count_files.settings import TERM_WIDTH
from count_files.utils.file_handlers import get_file_extension, check_pattern_matching


class BaseOS(object):
    """Superclass to work with operating systems.

    Contains the basic methods of counting and searching files
    (common to all operating systems).
    Checking of hidden files and folders is implemented
    in subclasses for specific operating systems.

    An instance of this class can be used in an OS supported by Python,
    but in which the program has not been tested.
    In this case, the option to exclude hidden files and folders
    from counting or searching is not available.
    """

    name = 'BaseOS'

    def is_hidden_file_or_dir(self, *args, **kwargs) -> bool:
        """The function determines whether the file or folder in filepath is hidden.

        Overwritten in subclasses for certain OS.
        Windows: testing the FILE_ATTRIBUTE_HIDDEN for file or folder.
        Linux, Mac OS, iOS: testing at least for the dot character in path on Unix-like systems.

        :return: False by default for instance of BaseOS
        """
        return False

    def search_files(self, dirpath: str, extension: str, contains: List[str] = None, recursive: bool = True,
                     include_hidden: bool = False, case_sensitive: bool = False) -> Iterable[str]:
        """Find all files in a given directory with and without the extension.

        :param dirpath: full/path/to/folder
        :param extension: extension name (txt, py), '.'(without extension) or '..' (all extensions)
        :param contains: example ['substring', 'filename', 'startswith']
        substring to search in file path, where to search - 'path', 'filename' or 'extension',
        pattern type - 'startswith', 'endswith', 'contains'
        :param recursive: True(default) or False
        :param include_hidden: False -> exclude hidden, True -> include hidden, counting all files
        :param case_sensitive: False -> ignore case in extensions,
        True -> distinguish case variations in extensions
        :return: object <class 'generator'> with full paths to all found files
        """
        # this part used for -fe .. or -t .. (all extensions)
        # -pc/-fc/-ec substring (find_group)
        if extension == '..':
            for root, dirs, files in os.walk(dirpath):
                for f in files:
                    f_path = os.path.join(root, f)
                    if contains:
                        if not check_pattern_matching(file_name=f, file_path=f_path,
                                                      pattern_type=contains[2], substring=contains[0],
                                                      case_sensitive=case_sensitive, where=contains[1]):
                            continue
                    if not os.path.isfile(f_path):
                        continue
                    if include_hidden or not self.is_hidden_file_or_dir(f_path):
                        yield f_path
                if not recursive:
                    break
        # this part used for: -fe . or -fe extension_name, -t . or -t extension_name
        else:
            ext = extension if case_sensitive else extension.upper()
            for root, dirs, files in os.walk(dirpath):
                for f in files:
                    f_path = os.path.join(root, f)
                    f_extension = get_file_extension(f_path, case_sensitive=case_sensitive)
                    if f_extension != ext or not os.path.isfile(f_path):
                        continue
                    if include_hidden or not self.is_hidden_file_or_dir(f_path):
                        yield f_path
                if not recursive:
                    break

    def count_files_by_extension(self, dirpath: str, no_feedback: bool = False, recursive: bool = True,
                                 include_hidden: bool = False, case_sensitive: bool = False) -> Counter:
        """Count all files in a given directory by their extensions.

        :param dirpath: full/path/to/folder
        :param no_feedback: True or False(default, prints processed file names in one line)
        :param recursive: True(default, recursive search/count) or False
        :param include_hidden: False -> exclude hidden, True -> include hidden, counting all files
        :param case_sensitive: False -> ignore case in extensions, True -> distinguish case variations in extensions
        :return: Counter() with extensions (keys: str)and their frequencies (values: int)
        if case_sensitive(extensions are displayed as is):
        Counter({'txt': 15, 'py': 15, 'pyc': 13, '[no extension]': 8, ...})
        if not case_sensitive(default, in uppercase):
        Counter({'TXT': 15, 'PY': 15, 'PYC': 13, '[no extension]': 8, ...})
        """
        counters = Counter()
        dirpath = os.path.expanduser(dirpath)

        def count_file_extensions(files: Iterable[str], no_feedback: bool = no_feedback):
            for f in files:
                extension = get_file_extension(f, case_sensitive=case_sensitive)
                if extension == '.':
                    extension = '[no extension]'
                counters[extension] += 1
                if not no_feedback:
                    print("\r" + os.path.basename(f)[:TERM_WIDTH - 1].ljust(TERM_WIDTH - 1), end="")

        if recursive:
            if include_hidden:
                for root, dirs, files in os.walk(dirpath):
                    count_file_extensions(files)
            else:
                for root, dirs, files in os.walk(dirpath):
                    only_these = [f for f in files
                                  if not self.is_hidden_file_or_dir(os.path.join(root, f))]
                    count_file_extensions(only_these)
        else:
            with os.scandir(dirpath) as directory:
                # if True return all files
                if include_hidden:
                    only_these = [f for f in directory if f.is_file()]
                else:
                    only_these = [f for f in directory if f.is_file()
                                  and not self.is_hidden_file_or_dir(os.path.join(dirpath, f))]
                count_file_extensions(only_these)

        if not no_feedback:
            print("\r".ljust(TERM_WIDTH - 1))  # Clean the feedback text before proceeding.
        return counters


class WinOS(BaseOS):
    """Subclass to work with Windows."""

    name = 'WinOS'

    def is_hidden_file_or_dir(self, filepath: str) -> bool:
        """The function determines whether the file or folder in filepath is hidden.

        Windows: testing the FILE_ATTRIBUTE_HIDDEN for file or folder.
        If any parent folders of filepath is hidden
        def is_hidden_file_or_dir return True, even if it has visible final file/folder.
        If parent folders not hidden, but final file/folder is hidden also return True.

        Behavior of the function if the path does not exist.
        When searching through a parser, a check os.path.exists() is performed.
        When used separately, the function returns False if the path does not exist.

        If filepath is a local drive it returns True.
        is_hidden_file_or_dir('C:/') True , ...('C:') False
        is_hidden_file_or_dir('D:/') True, ...('D:') True
        :param filepath: full/path/to/file.txt or full/path/to_folder
        :return: True if hidden or False if not
        """
        # list with full paths of all parents in filepath except drive
        list_for_check = list(Path(filepath).parents)[:-1]
        list_for_check.append(Path(filepath))
        response = []
        for some_path in list_for_check:
            try:
                attrs = ctypes.windll.kernel32.GetFileAttributesW(str(some_path))
                assert attrs != -1
                result = bool(attrs & 2)
            except (AttributeError, AssertionError):
                result = False
            response.append(result)
        if any(response):
            return True
        return False


class UnixOS(BaseOS):
    """Subclass to work with Unix-like systems."""

    name = 'UnixOS'

    def is_hidden_file_or_dir(self, filepath: str) -> bool:
        """The function determines whether the file or folder in filepath is hidden.

        Linux, Mac OS, iOS: testing at least for the dot character in path on Unix-like systems.
        def is_hidden_file_or_dir('~/path/.to/file.txt') checking for the dot character in path,
        so if '/.' in path the entire folder is ignored, even if it has visible files.

        Behavior of the function if the path does not exist.
        When searching through a parser, a check os.path.exists() is performed.
        When used separately, the result depends on the presence of a "/." in the path.

        :param filepath: full/path/to/file.txt or full/path/to_folder
        :return: True if hidden or False if not
        """
        return bool('/.' in filepath)


def get_current_os():
    """The function to determine the OS in which the program operates.

    Used in CLI and tests.
    :return: an instance of the appropriate class to work with the current OS
    """
    if sys.platform.startswith('win'):
        current_os = WinOS()
    elif sys.platform.startswith('linux') or sys.platform.startswith('ios') \
            or sys.platform.startswith('darwin') or sys.platform.startswith('haiku'):
        current_os = UnixOS()
    else:
        # undefined
        current_os = BaseOS()
    return current_os
