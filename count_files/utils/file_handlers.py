#!/usr/bin/env python3
# encoding: utf-8
import ctypes
import os
import sys

from pathlib import Path
from typing import Iterable
from collections import Counter
from itertools import chain

from count_files.settings import SUPPORTED_TYPES, TERM_WIDTH


def get_file_extension(filepath: str, case_sensitive=False) -> str:
    """Extract only the file extension from a given path.

    Behavior:
    select2.3805311d5fc1.css.gz -> gz, .gitignore -> '.'
    Pipfile -> '.', .hidden_file.txt -> txt
    :param filepath: full/path/to/file
    :param case_sensitive: False -> ignore case in extensions, True -> distinguish case variations in extensions
    :return: extension name (txt, py) or '.' (for files without extension). If case_sensitive==False, return in uppercase.
    """
    extension = os.path.splitext(filepath)[1][1:]
    if extension:
        if case_sensitive:
            return extension
        else:
            return extension.upper()
    else:
        return '.'


def is_supported_filetype(extension: str) -> bool:
    """
    Return a True if the given file extension has a supported file preview

    :param extension:
    :return: True if we have a preview procedure for the given file type, False otherwise.
    """
    return extension in list(chain.from_iterable(SUPPORTED_TYPES.values()))


def human_mem_size(num: int, suffix='B') -> str:
    """Return a human readable memory size in a string.

    Initially written by Fred Cirera, modified and shared by Sridhar Ratnakumar
    (https://stackoverflow.com/a/1094933/6167478), edited by Victor Domingos.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num = num / 1024.0

    return "%.1f%s%s" % (num, 'Yi', suffix)


def search_files(dirpath: str, extension: str, recursive: bool, include_hidden: bool, case_sensitive: bool) -> Iterable[str]:
    """Find all files in a given directory with and without the extension.

    :param dirpath: full/path/to/folder
    :param extension: extension name (txt, py), '.'(without extension) or '..' (all extensions)
    :param recursive: True(default) or False
    :param include_hidden: False -> exclude hidden, True -> include hidden, counting all files
    :param case_sensitive: False -> ignore case in extensions, True -> distinguish case variations in extensions
    :return: object <class 'generator'>
    """
    # in fact this part do the same as def count_files_by_extension(except counters) if it called
    # directly -> search_files('full/path/to/folder', '..', recursive=True, include_hidden=True)
    # this part used for -fe .. (all extensions)
    # this is equivalent to the def count_files_by_extension, but instead of a table, it returns all paths
    if extension == '..':
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                f_path = os.path.join(root, f)
                if not os.path.isfile(f_path):
                    continue
                if include_hidden or not is_hidden_file_or_dir(f_path):
                    yield f_path
            if not recursive:
                break
    # this part used for -fe . and -fe extension_name
    else:
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                if not case_sensitive:
                    extension = extension.upper()
                f_path = os.path.join(root, f)
                f_extension = get_file_extension(f_path, case_sensitive=case_sensitive)
                if f_extension != extension or not os.path.isfile(f_path):
                    continue
                if include_hidden or not is_hidden_file_or_dir(f_path):
                    yield f_path
            if not recursive:
                break


def count_files_by_extension(dirpath: str, no_feedback: bool, recursive=False, include_hidden=True, case_sensitive=False) -> Counter:
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
                print("\r"+os.path.basename(f)[:TERM_WIDTH-1].ljust(TERM_WIDTH-1), end="")

    if recursive:
        if include_hidden:
            for root, dirs, files in os.walk(dirpath):
                count_file_extensions(files)
        else:
            for root, dirs, files in os.walk(dirpath):
                only_these = [f for f in files
                              if not is_hidden_file_or_dir(os.path.join(root, f))]
                count_file_extensions(only_these)
    else:
        with os.scandir(dirpath) as directory:
            # if True return all files
            if include_hidden:
                only_these = [f for f in directory if f.is_file()]
            else:
                only_these = [f for f in directory if f.is_file()
                              and not is_hidden_file_or_dir(os.path.join(dirpath, f))]
            count_file_extensions(only_these)
    
    print("\r".ljust(TERM_WIDTH-1))  # Clean the feedback text before proceeding.
    return counters


def is_hidden_file_or_dir(filepath: str) -> bool:
    """The function determines whether the file or folder in filepath is hidden.

    Windows: testing the FILE_ATTRIBUTE_HIDDEN for file or folder.
    Note: if any parent folders of filepath is hidden
    def is_hidden_file_or_dir return True, even if it has visible final file/folder.
    If parent folders not hidden, but final file/folder is hidden also return True.
    (discussion: https://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection)

    Linux: testing at least for the dot character in path on Unix-like systems.
    Note: for Linux def is_hidden_file_or_dir('~/path/.to/file.txt') checking for the dot character in path,
    so if '/.' in path the entire folder is ignored, even if it has visible files.

    Note: the behavior of the function if the path does not exist.
    When searching through a parser, a check os.path.exists() is performed.
    Windows: when used separately, the function returns False if the path does not exist.
    Linux, Mac OS: when used separately, the result depends on the presence of a "/." in the path.

    :param filepath: full/path/to/file.txt or full/path/to_folder
    :return: True if hidden or False if not
    """
    platform_name = sys.platform
    filepath = os.path.normpath(filepath)
    if platform_name.startswith('win'):
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
    elif platform_name.startswith('linux'):
        return bool('/.' in filepath)
    elif platform_name.startswith('darwin'):
        return bool('/.' in filepath)
