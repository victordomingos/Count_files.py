#!/usr/bin/env python3
# encoding: utf-8
"""Count Files.
A command-line interface (CLI) utility.
Supported operating systems: Linux, Mac OS, Windows.
It may also be used on iOS (iPhone/iPad) using the StaSh command-line in the Pythonista 3 app.
Main functions:
total counting of files (the total number of files it the directory);
file counting by extension (a table with file extensions sorted by frequency or alphabetically);
file searching by extension(a list with file paths, optional: file sizes, preview for text files).
Features:
counting or searching files with a specific extension, files without an extension,
all files regardless of the extension;
recursive and non-recursive counting or searching;
enable or disable the search or counting in hidden files and folders;
process the file extensions with case-sensitive or case-insensitive mode;
enable or disable the program's operating indicator (feedback).

© 2018-2019 Victor Domingos & Nataliia Bondarenko
MIT License
"""
import os
from sys import platform
from argparse import ArgumentParser, Namespace
from typing import TypeVar, Union
from pathlib import Path
from textwrap import fill

from count_files.utils.file_handlers import is_supported_filetype, get_pattern_substring_and_type, \
    get_find_group_values
from count_files.utils.viewing_modes import show_2columns, show_start_message, \
    show_result_for_total, show_result_for_search_files
from count_files.platforms import get_current_os
from count_files.settings import SUPPORTED_TYPE_INFO_MESSAGE, NOT_SUPPORTED_TYPE_MESSAGE, \
    DEFAULT_PREVIEW_SIZE, START_TEXT_WIDTH, SUPPORTED_PATTERN_MESSAGE, WARNING
from count_files.utils.help_system_extension import search_in_help, print_help_text
from count_files.utils.help_text import topics
from count_files.utils.decorators import exceptions_decorator


parser = ArgumentParser(
    prog='count-files',
    description='Count files, grouped by extension, in a directory. By '
                'default, it will count files recursively in current '
                'working directory and all of its subdirectories, and '
                'will display a table showing the frequency for each file '
                'extension (e.g.: .txt, .py, .html, .css) and the total '
                'number of files found. For supported operating systems '
                '(Linux, Mac OS, iOS, Windows), '
                'any hidden files or folders are ignored by default. '
                'For other operating systems this option is not available, '
                'and as a result all existing files will be included. '
                'Also by default file extensions are treated with no case sensitiveness.')

parser.add_argument('-v', '--version', action='version', version=__import__('count_files').__version__)

parser.add_argument('-st', '--supported-types', action='store_true',
                    help=topics['supported-types']['short'])

parser.add_argument('-fp', '--find-patterns', action='store_true',
                    help=topics['find-patterns']['short'])


parser.add_argument('path', nargs='?', default=os.getcwd(), type=str,
                    help=topics['path']['short'])

parser.add_argument('-a', '--all', action='store_true', default=False,
                    help=topics['all']['short'])

parser.add_argument('-nr', '--no-recursion', action='store_true', default=False,
                    help=topics['no-recursion']['short'])

parser.add_argument('-c', '--case-sensitive', action='store_true', default=False,
                    help=topics['case-sensitive']['short'])

parser.add_argument('-nf', '--no-feedback', action='store_true', default=False,
                    help=topics['no-feedback']['short'])

parser.add_argument('-ah', '--args-help', type=str, dest='topic',
                    help=topics['args-help']['short'])

total_group = parser.add_argument_group('Total number of files'.upper(),
                                        description=topics['total-group']['short'])

total_group.add_argument('-t', '--total', dest="extension", type=str,
                         help=topics['total']['short'])


count_group = parser.add_argument_group('File counting by extension'.upper(),
                                        description=topics['count-group']['short'])

count_group.add_argument('-alpha', '--sort-alpha', action='store_true', default=False,
                         help=topics['sort-alpha']['short'])

search_group = parser.add_argument_group('File searching by extension'.upper(),
                                         description=topics['search-group']['short'])

search_group.add_argument('-fe', '--file-extension', type=str,
                          help=topics['file-extension']['short'])

search_group.add_argument('-p', '--preview', action='store_true', default=False,
                          help=topics['preview']['short'])

search_group.add_argument('-ps', '--preview-size', type=int, default=DEFAULT_PREVIEW_SIZE,
                          help=topics['preview-size']['short'])

search_group.add_argument('-fs', '--file-sizes', action='store_true', default=False,
                          help=topics['file-sizes']['short'])

find_group = parser.add_argument_group('Find substring in a path, file name or extension'.upper(),
                                       description=topics['find-group']['short'])

# now simply checking x in string, but may accept list of substrings
# group arguments are used separately from each other
find_group.add_argument('-pc', '--path-contains', type=str, dest='path_substring',
                        help=topics['path-contains']['short'])
find_group.add_argument('-fc', '--filename-contains', type=str, dest='filename_substring',
                        help=topics['filename-contains']['short'])
find_group.add_argument('-ec', '--extension-contains', type=str, dest='extension_substring',
                        help=topics['extension-contains']['short'])

parser._positionals.title = parser._positionals.title.upper()
parser._optionals.title = parser._optionals.title.upper()

argparse_namespace_object = TypeVar('argparse_namespace_object', bound=Namespace)


@exceptions_decorator
def main_flow(*args: [argparse_namespace_object, Union[bytes, str]]):
    """Main application function.

    :param args: object <class 'argparse.Namespace'>,
    for tests param args - list with objects of <class 'str'>
    :return:
    Returns the processed data as text to the screen.
    Total number of files, table or list with file paths.
    Returns parser.exit(status=1):
    if path does not exist or there may be a typo in it,
    if the path has hidden folders and the argument --all is not specified,
    if the preview is not available for the specified file type.
    """
    args = parser.parse_args(*args)
    recursive = not args.no_recursion
    include_hidden = args.all
    sort_alpha = args.sort_alpha
    extension = args.file_extension
    current_os = get_current_os()
    if current_os.name == 'BaseOS':
        # the default option to exclude hidden files and folders is not implemented for undefined OS,
        # no need to call self.is_hidden_file_or_dir()
        include_hidden = True

    if args.supported_types:
        parser.exit(status=0, message=print_help_text(SUPPORTED_TYPE_INFO_MESSAGE))
    if args.find_patterns:
        parser.exit(status=0, message=print_help_text(SUPPORTED_PATTERN_MESSAGE))
    if args.topic:
        search_in_help(args.topic)
        parser.exit(status=0)

    if os.path.abspath(args.path) == os.getcwd():
        location = os.getcwd()
        loc_text = ' the current directory'
    else:
        location = os.path.expanduser(args.path)
        loc_text = ':\n' + os.path.normpath(location)

    if not os.path.exists(location):
        parser.exit(status=1, message=f'The path {location} '
                                      f'does not exist, or there may be a typo in it.')

    if not include_hidden and current_os.is_hidden_file_or_dir(location):
        # skip check if path is a local drive
        if platform.startswith('win') and len(Path(location).parents) == 0:
            pass
        else:
            parser.exit(status=1, message=f'\nNot counting any files, because {loc_text[2:]}'
                                          f' has hidden folders.\n'
                                          f'Use the --all argument to include hidden files and folders.')

    common_args = dict(dirpath=location, include_hidden=include_hidden,
                       recursive=recursive, case_sensitive=args.case_sensitive)
    show_result_for_search_args = dict(file_sizes=args.file_sizes, preview=args.preview,
                                       preview_size=args.preview_size)
    groups_args = [extension, args.extension,
                   args.path_substring, args.filename_substring, args.extension_substring]
    # 0(count) or 1(others)
    if len([arg for arg in groups_args if arg is not None]) > 1:
        parser.exit(status=1, message=print_help_text(WARNING))

    # Parser find_group: search for any folder, file of extension name in path
    find_group_args = any([args.path_substring, args.filename_substring, args.extension_substring])
    if find_group_args:
        where_and_substring = {'path': args.path_substring, 'filename': args.filename_substring,
                               'extension': args.extension_substring}
        substring, where = get_find_group_values(where_and_substring)
        pattern_type, substring = get_pattern_substring_and_type(substring)
        print(fill(show_start_message(value='..', group='find', contains=[substring, where, pattern_type], **common_args),
                   width=START_TEXT_WIDTH),
              end="\n\n")
        data = current_os.search_files(extension='..', contains=[substring, where, pattern_type], **common_args)
        # display the result as a list
        len_files = show_result_for_search_files(files=data, **show_result_for_search_args)
        return len_files

    # Parser total_group:
    # getting the total number of files for -t .. (all extensions), -t . and -t extension_name
    print("")
    if args.extension:
        print(fill(show_start_message(value=args.extension, group='total', **common_args),
                   width=START_TEXT_WIDTH),
              end="\n\n")
        data = current_os.search_files(extension=args.extension, **common_args)
        total_result = show_result_for_total(data, args.no_feedback)
        return total_result

    # Parser search_group: search and list files by extension
    if extension:
        # list of all found file paths - enabled by default,
        # optional: information about file sizes, file preview, size specification for file preview
        if args.preview:
            if extension == '.' or not is_supported_filetype(extension.lower()):
                parser.exit(status=1, message=print_help_text(NOT_SUPPORTED_TYPE_MESSAGE))

        print(fill(show_start_message(value=extension, **common_args), width=START_TEXT_WIDTH), end="\n\n")
        # getting data list for -fe .. (all extensions), -fe . and -fe extension_name
        data = (f for f in current_os.search_files(extension=extension, **common_args))
        # display the result as a list
        len_files = show_result_for_search_files(files=data, **show_result_for_search_args)
        return len_files

    # Parser count_group: counting all files by extension
    print(fill(show_start_message(value=None, **common_args), width=START_TEXT_WIDTH), end="\n\n")

    data = current_os.count_files_by_extension(no_feedback=args.no_feedback, **common_args)
    # if empty sequence
    if not data:
        parser.exit(status=0, message="Oops! We have no data to show...\n")
        
    total_occurrences = sum(data.values())
    max_word_width = max(map(len, data.keys()))

    # display the result as a table
    if sort_alpha:
        # sort extensions alphabetically, with uppercase versions on top
        sort_key = lambda data: (data[0].casefold(), data[0])
        data = sorted(data.items(), key=sort_key)
    else:
        # sort extensions by frequency for each file extension
        data = data.most_common()
    show_2columns(data, max_word_width, total_occurrences)
    parser.exit(status=0)


if __name__ == "__main__":
    main_flow()
