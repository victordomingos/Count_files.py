#!/usr/bin/env python3
# encoding: utf-8
"""Functions designed to display the results of the program or CLI messages.

CLI viewing modes:
    count - def show_2columns
table with file extensions sorted by frequency or alphabetically
    search - def show_result_for_search_files
list of all found file paths(with sizes),
preview, total number of files and size info(summary)
    total - def show_result_for_total
total number of all found file paths
    help extension - def show_help_columns
table with the specified number of columns to display available help topics
(argument or group name, sort words)

CLI messages:
def show_start_message
    message with information about selected counting or searching CLI arguments

Other utilities:
def human_mem_size
    return a human readable memory size in a string for os.path.getsize(file_path)
"""
import os
from typing import Iterable, List
from textwrap import wrap

from count_files.utils.file_preview import generate_preview
from count_files.settings import TERM_WIDTH, DEFAULT_PREVIEW_SIZE
from count_files.settings import DEFAULT_EXTENSION_COL_WIDTH
from count_files.settings import DEFAULT_FREQ_COL_WIDTH, MAX_TABLE_WIDTH


def human_mem_size(num: int, suffix: str = 'B') -> str:
    """Return a human readable memory size in a string.

    Initially written by Fred Cirera, modified and shared by Sridhar Ratnakumar
    (https://stackoverflow.com/a/1094933/6167478), edited by Victor Domingos.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num = num / 1024.0

    return "%.1f%s%s" % (num, 'Yi', suffix)


def show_start_message(value: [None, str], case_sensitive: bool, recursive: bool, include_hidden: bool,
                       dirpath: str, group: str = None, contains: List[str] = None) -> str:
    """Displays a message with information about selected counting or searching CLI arguments.

    :param value: str for args.total or args.file_extension, for table - None.
    :param case_sensitive: args.case_sensitive
    :param recursive: args.no_recursion
    :param include_hidden: args.all
    :param dirpath: path argument
    :param group: 'total', 'find' or None
    :param contains: contains=[substring, where, pattern_type]
    :return: prints information message
    """
    wi = 'or without it'
    case = 'case-sensitive' if case_sensitive else 'case-insensitive'
    all_e = ' without any extension'
    h = ' including hidden files and directories'
    nh = ' ignoring hidden files and directories'

    if group == 'total':
        r = f'Recursively counting total number of files'
        nr = 'Counting total number of files'
        e = f' with{" (" + case + ")" if value not in [".", ".."] else ""} ' \
            f'extension {"." + value if value != ".." else wi}'
    # search for any folder or file name in path
    elif group == 'find':
        if 'with' in contains[2]:
            pt = contains[2].split('w')[0] + " with"
        else:
            pt = contains[2].split('s')[0]
        r = f'Recursively searching for {contains[1]}s that {pt} the substring "{contains[0]}"'
        nr = f'Searching for {contains[1]}s that {pt} the substring "{contains[0]}"'
        c = f'{"(" + case + ")" if {case} else ""}'
        message = f'{r if recursive else nr} {c},' \
                  f'{h if include_hidden else nh}, in {dirpath}'
        return message
    # count_group and search_group
    else:
        action = 'searching' if value else 'counting'
        r = f'Recursively {action} all files'
        nr = f'{action.title()} files'
        e = f' with{" (" + case + ")" if value not in [".", ".."] else ""} ' \
            f'extension {"." + value if value != ".." else wi}' if value else ''

    message = f'{r if recursive else nr}{e if value != "." else all_e},' \
              f'{h if include_hidden else nh}, in {dirpath}'

    return message


def show_2columns(data: List[tuple],
                  max_word_width: int, total_occurrences: int,
                  term_width: int = TERM_WIDTH):
    """Displays a sorted table with file extensions.

    :param data: list with tuples
    default in uppercase: [('TXT', 24), ('PY', 17), ('PYC', 13), ...]
    with --case-sensitive as is: [('txt', 23), ('py', 17), ('pyc', 13), ...]
    :param max_word_width: the longest extension name
    :param total_occurrences: total number of files found
    :param term_width: the size of the terminal window
    :return: the processed data as text to the screen.
    """
    if not data:
        print("Oops! We have no data to show...\n")
        return

    max_word_width = max(DEFAULT_EXTENSION_COL_WIDTH, max_word_width)
    freq_col_width = max(DEFAULT_FREQ_COL_WIDTH, len(str(total_occurrences)))
    ext_col_width = min((term_width - freq_col_width - 5),
                        max_word_width,
                        MAX_TABLE_WIDTH)

    header = f" {'EXTENSION'.ljust(ext_col_width)} | {'FREQ.'.ljust(freq_col_width)} "
    sep_left = (ext_col_width + 2) * '-'
    sep_center = "+"
    sep_right = (freq_col_width + 2) * '-'
    sep = sep_left + sep_center + sep_right
    print(header)
    print(sep)

    for word, freq in data:
        if len(word) <= ext_col_width:
            print(f" {word.ljust(ext_col_width)} | {str(freq).rjust(freq_col_width)} ")
        else:
            head = f" {word[0: ext_col_width]} | {str(freq).rjust(freq_col_width)}"
            word_tail = wrap(word[ext_col_width:],
                             width=ext_col_width,
                             initial_indent=' ' * 2,
                             subsequent_indent=' ' * 2)
            print(head)
            for line in word_tail:
                print(f" {line.ljust(ext_col_width)} | {' '.rjust(freq_col_width)}")

    print(sep)
    line = f" {'TOTAL:'.ljust(ext_col_width)} | {str(total_occurrences).rjust(freq_col_width)} "
    print(line)
    print(sep + "\n")
    return


def show_result_for_search_files(files: Iterable[str],
                                 file_sizes: bool = False,
                                 preview: bool = False,
                                 preview_size: int = DEFAULT_PREVIEW_SIZE) -> int:
    """Print list of all found file paths(with sizes),
    preview, total number of files and size info(summary).

    :param files: list with paths
    :param file_sizes: True -> show size info, False -> don't show size info
    :param preview: optional, args.preview, True or False
    :param preview_size: optional, args.preview_size, number
    :return: len(files), print list with paths(default),
    get preview and file_sizes if specified.

    full/path/to/file1.extension (... KiB)
    –––––––––––––––––––––––––––––––––––
    preview, if preview=True and supported type
    –––––––––––––––––––––––––––––––––––
    full/path/to/file2.extension (... KiB)
    ...
    Found ... file(s).
    Total combined size: ... KiB.
    Average file size: ... KiB (max: ... KiB, min: ... B).
    """
    files_amount = 0
    sizes = []
    try:
        for f_path in files:
            files_amount += 1
            if file_sizes:
                file_size = os.path.getsize(f_path)
                sizes.append(file_size)
                s = f'({human_mem_size(file_size)})'
            filepath = str(f_path).strip("\r")
            print(f'{os.path.normpath(filepath)} {s if file_sizes else ""}')
            if preview:
                print('–––––––––––––––––––––––––––––––––––')
                print(generate_preview(str(f_path), max_size=preview_size))
                print("–––––––––––––––––––––––––––––––––––\n")
    except StopIteration:
        print(f"\nNo files were found in the specified directory.\n")
        return 0
    if files_amount == 0:
        print(f"\nNo files were found in the specified directory.\n")
        return 0
    print(f"\n   Found {files_amount} file(s).", end="\n")
    if file_sizes:
        total_size = sum(sizes)
        h_total_size = human_mem_size(total_size)
        avg_size = human_mem_size(int(total_size / files_amount))

        h_max = human_mem_size(max(sizes))
        h_min = human_mem_size(min(sizes))

        print(f"   Total combined size: {h_total_size}.")
        print(f"   Average file size: {avg_size} (max: {h_max}, min: {h_min}).",
              end="\n\n")
    else:
        print("")
    return files_amount


def show_result_for_total(files: Iterable[str], no_feedback: bool) -> int:
    """Print feedback and total number of all found file paths for Parser total_group.

    :param files: object <class 'generator'> with full paths to all found files
    :param no_feedback: True or False(default, prints processed file paths in one line)
    :return: len(files), files amount
    """
    if not no_feedback:
        files_amount = 0
        for f in files:
            files_amount += 1
            print("\r" + f[:TERM_WIDTH - 1].ljust(TERM_WIDTH - 1), end="")
        print("\r".ljust(TERM_WIDTH))  # Clean the feedback text before proceeding.
    else:
        files_amount = len(list(files))
    if files_amount == 0:
        print(f"No files were found in the specified directory.\n")
    else:
        print(f'   Found {files_amount} file(s).', end="\n\n")
    return files_amount


def show_help_columns(column_version: List[str], list_version: List[str],
                      num_columns: int = 2, term_width: int = TERM_WIDTH) -> str:
    """Displays a table with the specified number of columns.

    Suitable for a list with short words.
    If the words are very long and/or there are many columns
    (the width of the table is greater than the width of the terminal),
    then the data is displayed in a list.
    When used in the help extension, the list is displayed using the textwrap fill().
    For a table, the width of each column is equal
    to the width of the longest word in the list.

    :param column_version: list with words
    The first in the list may be the names of the columns.
    Example: column_version = ['LONG', 'SHORT',
                               'path', 'path',
                               'all', 'a',
                               'args-help', 'ah']
    :param list_version: list with words
    :param num_columns: number of columns
    :param term_width: width of the terminal; also required for testing
    :return:
    """
    max_word_width = max(map(len, column_version))
    if (max_word_width * num_columns + 3 * num_columns) > term_width:
        return ', '.join(list_version)
    text_table = " "
    for count, item in enumerate(column_version, 1):
        text_table += item.ljust(max_word_width + 3)
        if count % num_columns == 0 or count == len(column_version):
            text_table += "\n "
    return text_table
