"""HELP SYSTEM EXTENSION TEXT."""
from count_files.settings import DOCUMENTATION_URL, DEFAULT_PREVIEW_SIZE
from count_files.utils.viewing_modes import show_help_columns


docs_text = f"""COUNT FILES HELP.

More about Count Files Help usage(this section)
    help> help
To quit this utility, just type "quit"
    help> quit
    
SEARCH FOR ARGUMENTS:
Search in help text by topic. Topic - argument or group name.
Show more detailed help text: Topic must be in lower case.
    help> topic
Show short help text: Topic must be in upper case or with one letter in upper case.
    help> TOPIC
Search by short/long argument name:
    help> st
    help> supported-types
  
SORTING ARGUMENTS:
Get all count arguments and group description:
    help> count
All certain words for sorting:
Sorting arguments by group, including group description - count, search or total.
Get only group description - count-group or cg, search-group or sg, total-group or tg.
Get all group descriptions - groups.
Sorting arguments by purpose - service, common, special.
Sorting arguments by type - positional or optional

ALSO USE:
Get a list of available topics for searching or sorting.
    help> list
More about search by short/long argument name.
    help> args
More about sorting arguments by purpose or type.
    help> sort
Get the standard argparse help with a brief description of all the arguments.
    count-files --help
Web Docs in English, Portuguese, Russian and Ukrainian:
    {DOCUMENTATION_URL}
"""

arguments = [
             # column titles
             'LONG', 'SHORT',
             # positional
             'path', 'path',
             # optional
             'all', 'a', 'case-sensitive', 'c',
             'file-extension', 'fe', 'filename-match', 'fm', 'file-sizes', 'fs',
             'group', 'g', 'help', 'h', 'help-cmd', 'hc',
             'no-feedback', 'nf', 'no-recursion', 'nr',
             'preview', 'p', 'preview-size', 'ps', 'show-folders', 'sf',
             'sort-alpha', 'alpha', 'supported-types', 'st', 'total', 't', 'total-size', 'ts', 'version', 'v']

docs_args_text = f"""COUNT FILES HELP(ARGS).

AVAILABLE ARGUMENT NAMES:

{show_help_columns(column_version=arguments, list_version=arguments[3:], num_columns=2)}

SEARCH BY ARGUMENT NAME:
Short argument name.
    help> st
Long argument name.
    help> supported-types
Partial argument name if it consists of two words.
    help> supported
    help> types
Get help text about --help argument. Use short argument name:
    help> h
Get help text about --help-cmd argument. Use short argument name:
    help> hc
"""

sort_words = [
    'SORT BY PURPOSE', 'SORT BY TYPE',
    'service', 'positional',
    'common', 'optional',
    'special'
]

docs_sort_text = f"""COUNT FILES HELP(SORT).

AVAILABLE SORT WORDS:

{show_help_columns(column_version=sort_words, list_version=sorted(sort_words[2:]), num_columns=2)}

SORTING ARGUMENTS BY PURPOSE:
Service arguments: display of help, version of the program etc.
(h or help, ah or args-help, v or version, st or supported-types)
    help> service
Common arguments: directory path and sorting settings that are common to search and count.
(path, a or all, c or case-sensitive, nr or no-recursion, nf or no-feedback)
    help> common
Special arguments: arguments for counting or searching files.
Count by extension: alpha or sort-alpha, g or group;
Total number of files: t or total, sf or show-folders, ts or total-size;
Search by extension: fe or file-extension, fm or filename-match, fs or file-sizes, p or preview, ps or preview-size.
    help> special

SORTING ARGUMENTS BY TYPE:
    help> positional
    help> optional
"""

group_names = [
    'GROUP DESC', 'ARGS AND DESC',
    # cg, count-group - certain group description
    # count - sorting by group, including group description
    'cg, count-group', 'count',
    'sg, search-group', 'search',
    'tg, total-group', 'total',
    # all groups
    'groups'
]

docs_general_text = f"""ALSO USE:
Get the standard argparse help with a brief description of all the arguments.
    count-files --help
Get this Count Files Help.
    help> help
Get a list of available topics for searching or sorting.
    help> list
Web Docs in English, Portuguese, Russian and Ukrainian:
    {DOCUMENTATION_URL}
"""

docs_list_text = f"""COUNT FILES HELP(LIST).

AVAILABLE ARGUMENT NAMES:

{show_help_columns(column_version=arguments, list_version=arguments[3:], num_columns=2)}

AVAILABLE SORT WORDS:

{show_help_columns(column_version=sort_words, list_version=sorted(sort_words[2:]), num_columns=2)}

AVAILABLE GROUP NAMES:

{show_help_columns(column_version=group_names, list_version=sorted(group_names[2:]), num_columns=2)}

{docs_general_text}
"""

# all argument and group names descriptions(short and long help text)
topics = {
    'help': {
        'name': '-h, --help',
        'short': 'Built-in argparse help system with a brief description of all the arguments. '
                 'Show help message and exit.',
        'long': 'Built-in argparse help system with a brief description of all the arguments. '
                'Show help message and exit. '
                'Usage: count-files -h or count-files --help.'
    },
    'help-cmd': {
        'name': '-hc, --help-cmd',
        'short': 'Search in help by topic - argument or group name(count, search, total). '
                 'Start interactive help.',
        'long': 'Search in help by topic - argument or group name(count, search, total). '
                'Start interactive help. Usage: count-files -hc or count-files --help-cmd.'
    },
    'version': {
        'name': '-v, --version',
        'short': "Show program's version number and exit.",
        'long': "Show program's version number and exit. "
                'Usage: count-files -v or count-files --version.'
    },
    'supported-types': {
        'name': '-st, --supported-types',
        'short': 'The list of currently supported file types for preview.',
        'long': 'Show a list of currently supported file types for preview and exit. '
                'Usage: count-files -st or count-files --supported-types.'
    },
    'path': {
        'name': 'path',
        'short': 'The path to the folder containing the files to be counted.',
        'long': 'The path to the folder containing the files to be counted. '
                'If you leave this argument empty, it will scan the current working directory. '
                "To process files in the user's home directory, you can use ~ (tilde). "
                'For example: count-files ~/Documents <arguments>. '
                'Common argument for counting and searching by extension '
                'or counting the total number of files.'
    },
    'all': {
        'name': '-a, --all',
        'short': 'Include hidden files and directories.',
        'long': 'Include hidden files and directories. '
                'By default, it will ignore files and directories that are supposed to be hidden. '
                'In Windows, files and directories considered hidden by this application '
                'are those for which the FILE_ATTRIBUTE_HIDDEN attribute is set to true. '
                'In Linux, macOS, iOS and other Unix-like operating systems, '
                'a file or directory is considered to be hidden if its name starts with a "." (dot). '
                'Common argument for counting and searching by extension '
                'or counting the total number of files.'
    },
    'no-recursion': {
        'name': '-nr, --no-recursion',
        'short': "Don't recurse through subdirectories.",
        'long': "The optional -nr or --no-recursion switch argument "
                "tells the application not to scan recursively through the subdirectories. "
                'Common argument for counting and searching by extension '
                'or counting the total number of files.'
    },
    'case-sensitive': {
        'name': '-c, --case-sensitive',
        'short': 'Treat file extensions with case sensitiveness.',
        'long': 'The names of extensions are case insensitive by default. '
                'The results for ini and INI will be the same. '
                'To distinguish between similar extensions in different cases, '
                'use the -c or --case-sensitive switch argument. '
                'Common argument for counting and searching by extension '
                'or counting the total number of files.'
    },
    'no-feedback': {
        'name': '-nf, --no-feedback',
        'short': "Turns off the program's operating indicator (printing processed file names in one line).",
        'long': "Don't show the program's operating indicator (printing processed file names in one line). "
                'Feedback is available by default for counting files by extension '
                '(table) and for counting the total number of files (-t or --total). '
                'This option disables it. '
                'For searching by extension feedback is a list of the found file paths.'
    },
    'total-group': {
        'name': 'Total number of files',
        'short': 'Displaying the number of files that either have a certain extension or no extension at all.',
        'long': 'Displaying the number of files that either have a certain extension or no extension at all. '
                'To count the total number of files, '
                'the number of files with a specific extension '
                'or the number of files without any extension '
                'you can use the -t or --total argument and specify the name of the extension. '
                'Usage: count-files [-a, --all] [-c, --case-sensitive] '
                '[-nr, --no-recursion] [-nf, --no-feedback] '
                '[-t EXTENSION, --total EXTENSION] [-sf, --show-folders] '
                '[-ts, --total-size] [path].'
    },
    'total': {
        'name': '-t EXTENSION, --total EXTENSION',
        'short': 'Get the total number of files with given extension in the directory. '
                 'As the extension name: use a single dot "." for files without an extension '
                 'or two dots ".." for all the files, regardless of the extension.',
        'long': 'Get the total number of files in the directory. '
                'If you only need the total number of all files, '
                'or the number of files with a certain extension or without it. '
                'To count the total number of files, you must specify the name of the extension. '
                'Example: count-files --total txt ~/Documents <arguments>. '
                'Use a single dot "." to get the total number of files that do not have an extension. '
                'Example: count-files --total . ~/Documents <arguments>. '
                'Use two dots without spaces ".." to get the total number of files, with or without a file extension. '
                'Example: count-files --total .. ~/Documents <arguments>. '
    },
    'show-folders': {
        'name': '-sf, --show-folders',
        'short': 'Show the list of folders in which the found files are located, '
                 'and the number of found files in each folder.',
        'long': 'Show the list of folders in which the found files are located. '
                'In addition, the number of found files in each folder is displayed. '
                'When recursively counting all files(--total ..) and using the --show-folders argument, '
                'all folders containing files are displayed. '
                'To include hidden folders, also add the --all argument. '
                'Example: count-files --total py --show-folders ~/Documents <arguments>.'
    },
    'total-size': {
        'name': '-ts, --total-size',
        'short': 'Show the total combined size of files found using the -t or --total argument.',
        'long': 'Show the total combined size of files found using the -t or --total argument. '
                'Additional information: average, minimum and maximum file size. '
                'Example: count-files --total txt --total-size ~/Documents <arguments>.'
    },
    'count-group': {
        'name': 'File counting by extension',
        'short': 'Counting all files in the specified directory, by file extension. '
                 'By default, it displays some feedback while scanning and '
                 'it presents a table with file extensions sorted by frequency.',
        'long': 'Counting all files in the specified directory, by file extension. '
                'By default, it displays some feedback while scanning and '
                'it presents a table with file extensions sorted by frequency '
                '(e.g.: .txt, .py, .html, .css) and the total number of files found. '
                'All file extensions in the table will be displayed in uppercase (default). '
                'Example: count-files <arguments>. '
                'Usage: count-files [-a, --all] [-alpha, --sort-alpha] [-g, --group] '
                '[-c, --case-sensitive] [-nr, --no-recursion] [-nf, --no-feedback] [path].'
    },
    'sort-alpha': {
        'name': '-alpha, --sort-alpha',
        'short': 'Sort the table alphabetically, by file extension.',
        'long': 'By default, result of file counting by extension is a table '
                'that lists all the file extensions found '
                'and displays the frequency for each file extension. '
                'To sort the extensions alphabetically, use the -alpha or --sort-alpha argument. '
                'Example: count-files ---sort-alpha ~/Documents <arguments>.'
    },
    'group': {
        'name': '-g, --group',
        'short': 'Group file extensions by type (e.g. images, videos).',
        'long': 'Group file extensions by type: archives, audio, videos, data, documents, '
                'executables, fonts, images, Python related extensions, videos, and other files. '
                'Example: count-files --group ~/Documents <optional arguments>.'},
    'search-group': {
        'name': 'File searching by extension or by pattern',
        'short': 'Search for files with a given extension or files matching a specific pattern. '
                 'By default, it presents a simple list with full file paths.',
        'long': 'Searching for files that have a given extension or files matching a specific pattern. '
                'This utility can be used to search for files that have a certain file extension '
                '(using -fe or --file-extension). '
                'You can also search for files using Unix shell-style wildcards: *, ?, [seq], [!seq] '
                '(-fm or --filename-match argument). '
                '* - matches everything (zero or more occurrences of any character), '
                '? - matches any single character, '
                '[seq] - matches any character in seq, [!seq] - matches any character not in seq. '
                'For a literal match, wrap the meta-characters in brackets. '
                'For example, "[?]" matches the character "?". '
                'Optionally, you can get a short preview for text files(-p or --preview). '
                'The size of the preview text sample can be customized '
                'by using the -ps or --preview-size argument '
                'followed by an integer number specifying the number of characters to present. '
                'By default, the result of a search is a list of the full paths of the files found. '
                'If you need information about the size of the files, '
                'use the -fs or --file-sizes argument. '
                'Usage: count-files [-a, --all] [-c, --case-sensitive] '
                '[-nr, --no-recursion] [-fe FILE_EXTENSION, --file-extension FILE_EXTENSION] '
                '[-fm PATTERN, --filename-match PATTERN] '
                '[-fs, --file-sizes] [-p, --preview] [-ps PREVIEW_SIZE, --preview-size PREVIEW_SIZE] [path].'
    },
    'file-extension': {
        'name': '-fe FILE_EXTENSION, --file-extension FILE_EXTENSION',
        'short': 'Searching and listing files by given extension in the directory. '
                 'As the extension name: use a single dot "." for files without an extension '
                 'or two dots ".." for all the files, regardless of the extension.',
        'long': 'Searching and listing files by extension. Specify the extension name. '
                'Example: count-files --file-extension txt ~/Documents <arguments>. '
                'Use a single dot "." to search for files without any extension. '
                'Files with names such as .gitignore, Procfile, _netrc '
                'are considered to have no extension in their name. '
                'Example: count-files --file-extension . ~/Documents <arguments>. '
                'Use two dots without spaces ".." to search for all files '
                'with or without file extensions in their names. '
                'Example: count-files --file-extension .. ~/Documents <arguments>. '
    },
    'filename-match': {
        'name': '-fm PATTERN, --filename-match PATTERN',
        'short': 'Searching and listing files matching a specific pattern, '
                 'using Unix shell-style wildcards: *, ?, [seq], [!seq].',
        'long': 'Searching and listing files matching a specific pattern, '
                'using Unix shell-style wildcards: *, ?, [seq], [!seq]. '
                '* - matches everything (zero or more occurrences of any character), '
                '? - matches any single character, '
                '[seq] - matches any character in seq, [!seq] - matches any character not in seq. '
                'For a literal match, wrap the meta-characters in brackets. '
                'For example, "[?]" matches the character "?". '
                'Example for .pyc, .pyo and similar files: '
                'count-files --filename-match *.py? ~/Documents <arguments>. '
                'Example for file names containing the word "test": '
                'count-files --filename-match *test* ~/Documents <arguments>.'
    },
    'preview': {
        'name': '-p, --preview',
        'short': 'Display a short preview (only available for text files when '
                 'using --file-extension or --filename-match arguments).',
        'long': 'Display a short preview (only for text files). '
                'Preview is available as an option when searching files '
                'using --file-extension or --filename-match arguments. '
                'The default text preview size depends on the terminal width settings. '
                'You can change this value by specifying the argument -ps or --preview-size. '
                'Example: count-files --file-extension txt --preview ~/Documents <arguments>.'
    },
    'preview-size': {
        'name': '-ps PREVIEW_SIZE, --preview-size PREVIEW_SIZE',
        'short': 'Specify the number of characters to be displayed from each found file '
                 'when using -p or --preview.',
        'long': 'Specify the number of characters to be displayed from each found file. '
                'Preview text files is available as an option when searching files '
                'using the --file-extension or --filename-match arguments with --preview argument. '
                f'Default preview size: {DEFAULT_PREVIEW_SIZE} characters (5 lines). '
                'The default text preview size depends on the terminal width settings. '
                'You can change this value by specifying the argument -ps or --preview-size '
                'followed by an integer (the number of characters to display from each file). '
                'Example: count-files --file-extension txt --preview --preview-size 50 '
                '~/Documents <arguments>.'
    },
    'file-sizes': {
        'name': '-fs, --file-sizes',
        'short': 'Show size info for each '
                 'found file when using --file-extension or --filename-match arguments.',
        'long': 'Show size info for each '
                'found file when using --file-extension or --filename-match arguments. '
                'Additional information: total combined size and average file size. '
                'Example: count-files --file-extension txt --file-sizes ~/Documents <arguments>.'
    }
}


# indexes for searching in help text and sorting arguments
indexes = {
    ('h', 'help', 'service', 'optional'):
        [topics['help']['name'], topics['help']['short'], topics['help']['long']],
    ('hc', 'help-cmd', 'service', 'optional'):
        [topics['help-cmd']['name'], topics['help-cmd']['short'], topics['help-cmd']['long']],
    ('v', 'version', 'service', 'optional'):
        [topics['version']['name'], topics['version']['short'], topics['version']['long']],
    ('st', 'supported-types', 'supported', 'types', 'service', 'optional'):
        [topics['supported-types']['name'], topics['supported-types']['short'], topics['supported-types']['long']],

    ('path', 'common', 'positional'):
        [topics['path']['name'], topics['path']['short'], topics['path']['long']],
    ('a', 'all', 'common', 'optional'):
        [topics['all']['name'], topics['all']['short'], topics['all']['long']],
    ('nr', 'no-recursion', 'no', 'recursion', 'common', 'optional'):
        [topics['no-recursion']['name'], topics['no-recursion']['short'], topics['no-recursion']['long']],
    ('c', 'case-sensitive', 'case', 'sensitive', 'common', 'optional'):
        [topics['case-sensitive']['name'], topics['case-sensitive']['short'], topics['case-sensitive']['long']],
    ('nf', 'no-feedback', 'no', 'feedback', 'common', 'optional'):
        [topics['no-feedback']['name'], topics['no-feedback']['short'], topics['no-feedback']['long']],

    ('total-group', 'groups', 'total', 'tg'):
        [topics['total-group']['name'], topics['total-group']['short'], topics['total-group']['long']],
    ('t', 'total', 'extension', 'special', 'optional'):
        [topics['total']['name'], topics['total']['short'], topics['total']['long']],
    ('sf', 'show-folders', 'show', 'folders', 'total', 'special', 'optional'):
        [topics['show-folders']['name'], topics['show-folders']['short'], topics['show-folders']['long']],
    ('ts', 'total-size', 'total', 'size', 'special', 'optional'):
        [topics['total-size']['name'], topics['total-size']['short'], topics['total-size']['long']],

    ('count-group', 'groups', 'count', 'cg'):
        [topics['count-group']['name'], topics['count-group']['short'], topics['count-group']['long']],
    ('alpha', 'sort-alpha', 'count', 'special', 'optional'):
        [topics['sort-alpha']['name'], topics['sort-alpha']['short'], topics['sort-alpha']['long']],
    ('g', 'group', 'count', 'special', 'optional'):
        [topics['group']['name'], topics['group']['short'], topics['group']['long']],

    ('search-group', 'groups', 'search', 'sg'):
        [topics['search-group']['name'], topics['search-group']['short'], topics['search-group']['long']],
    ('fe', 'file-extension', 'file', 'extension', 'search', 'special', 'optional'):
        [topics['file-extension']['name'], topics['file-extension']['short'], topics['file-extension']['long']],
    ('fm', 'filename-match', 'filename', 'match', 'pattern', 'search', 'special', 'optional'):
        [topics['filename-match']['name'], topics['filename-match']['short'], topics['filename-match']['long']],
    ('p', 'preview', 'search', 'special', 'optional'):
        [topics['preview']['name'], topics['preview']['short'], topics['preview']['long']],
    ('ps', 'preview-size', 'preview', 'size', 'search', 'special', 'optional'):
        [topics['preview-size']['name'], topics['preview-size']['short'], topics['preview-size']['long']],
    ('fs', 'file-sizes', 'file', 'sizes', 'search', 'special', 'optional'):
        [topics['file-sizes']['name'], topics['file-sizes']['short'], topics['file-sizes']['long']]
}


if __name__ == '__main__':
    pass
