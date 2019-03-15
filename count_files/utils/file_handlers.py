#!/usr/bin/env python3
# encoding: utf-8
import os
from itertools import chain
from typing import Tuple

from count_files.settings import SUPPORTED_TYPES


def get_file_extension(filepath: str, case_sensitive: bool = False) -> str:
    """Extract only the file extension from a given path.

    Behavior:
    select2.3805311d5fc1.css.gz -> gz, .gitignore -> '.'
    Pipfile -> '.', .hidden_file.txt -> txt
    Used in platforms.py and file_preview.py
    :param filepath: full/path/to/file or filename
    :param case_sensitive: False -> ignore case in extensions,
    True -> distinguish case variations in extensions
    :return: extension name (txt, py) or '.' (for files without extension).
    If case_sensitive==False, return in uppercase.
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
    """Return a True if the given file extension has a supported file preview.

    :param extension: extension name (txt, py), '.'(without extension) or '..' (all extensions)
    :return: True if we have a preview procedure for the given file type, False otherwise.
    """
    return extension in list(chain.from_iterable(SUPPORTED_TYPES.values()))


def get_pattern_substring_and_type(pattern: str) -> Tuple[str, str]:
    """The function determines the type of search pattern
    and the substring to search for in paths, file names or file extensions.

    Available patterns: substring*, *substring, *substring* or substring
    (startswith, endswith, contains).
    * - substitute character (mask "any number of any characters")

    :param pattern: find_group args value
    :return: pattern_type (startswith, endswith, contains),
    substring (search substring, cleared from substitute characters)
    """
    # search for "*" itself in path
    # "*" - start, "**" - end, "***" or more - contains 1 or more "*"
    if set(pattern) == {'*'}:
        if len(pattern) == 1:
            pattern_type = 'startswith'
            substring = '*'
        elif len(pattern) == 2:
            pattern_type = 'endswith'
            substring = '*'
        else:
            pattern_type = 'contains'
            substring = pattern[1: -1]
        return pattern_type, substring

    if pattern.startswith('*') and pattern.endswith('*'):
        pattern_type = 'contains'
        substring = pattern[1: -1]
    elif pattern.startswith('*'):
        pattern_type = 'endswith'
        substring = pattern[1:]
    elif pattern.endswith('*'):
        pattern_type = 'startswith'
        substring = pattern[:-1]
    else:  # if "*" is not specified, search as is
        pattern_type = 'contains'
        substring = pattern
    return pattern_type, substring


def check_pattern_matching(file_name: str, file_path: str, pattern_type: str,
                           substring: str, case_sensitive: bool, where: str) -> bool:
    """Filter path, filename or file extension by search pattern.

    Available patterns: substring*, *substring, *substring* (startswith, endswith, contains).
    * - substitute character (mask "any number of any characters")
    :param file_name: file name
    :param file_path: full/path/to/file
    :param pattern_type: startswith, endswith or contains
    :param substring: find_group args value
    :param case_sensitive: False -> ignore case in extensions,
    True -> distinguish case variations in extensions
    :param where: where to search by pattern
    If where == 'path':
    whole path if 'contains': search substring in folders, filename, extension
    else: path starts with substring or path ends with substring
    :return: True if path, filename or extension matches the search pattern, otherwise False
    """
    if where == 'extension':
        # return extension as is
        data = get_file_extension(file_name, case_sensitive=True)
        if data == '.':
            return False
    elif where == 'filename':
        data = os.path.splitext(file_name)[0]  # excluding extension
    else:  # where == 'path':
        data = file_path

    data = data if case_sensitive else data.lower()
    substring = substring if case_sensitive else substring.lower()

    if pattern_type == 'startswith':
        result = data.startswith(substring)
    elif pattern_type == 'endswith':
        result = data.endswith(substring)
    else:  # pattern_type == 'contains':
        result = substring in data
    return result


def handle_groups(kwargs: dict):
    """

    :param kwargs:
    :return: substring - find_group args value,
    where - 'path', 'filename', 'extension'
    """
    for k, v in kwargs.items():
        if kwargs.get(k):
            where = k
            substring = kwargs[k]
            return substring, where
