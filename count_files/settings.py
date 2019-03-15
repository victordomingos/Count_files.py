#!/usr/bin/env python3
# encoding: utf-8
import shutil
import platform


DOCUMENTATION_URL = 'https://github.com/victordomingos/Count-files#documentation'
BUG_REPORT_URL = 'https://github.com/victordomingos/Count-files/issues'

TERM_WIDTH = shutil.get_terminal_size((80, 24)).columns
DEFAULT_PREVIEW_SIZE = 5 * TERM_WIDTH  # 5 lines of text preview
START_TEXT_WIDTH = min(TERM_WIDTH, 100)
DEFAULT_EXTENSION_COL_WIDTH = 9
DEFAULT_FREQ_COL_WIDTH = 5
MAX_TABLE_WIDTH = 80

# ====================[ iOS/Pythonista specific settings ]====================
IPAD_FONT_SIZE = 15
IPHONE_FONT_SIZE = 10
IOS_WORKERS = 2
IOS_FONT = "Menlo"


if platform.system() == 'Darwin':
        if platform.machine().startswith('iPad'):
            device = "iPad"
        elif platform.machine().startswith('iP'):
            device = "iPhone"
        else:
            device = "mac"
else:
    device = "other"

if device in ("iPad", "iPhone"):
    # Adapt for smaller screen sizes in iPhone and iPod touch
    try:
        import ui
        import console
        if device == 'iPad':
            font_size = IPAD_FONT_SIZE
        else:
            font_size = IPHONE_FONT_SIZE
        console.set_font(IOS_FONT, font_size)
        screen_width = ui.get_screen_size().width
        char_width = ui.measure_string('.', font=(IOS_FONT, font_size)).width
        TERM_WIDTH = int(screen_width / char_width - 1.5) - 1
    except:
        pass

SUPPORTED_TYPES = {
    'all_extensions': ['..'],
    'no_extension': ['.'],
    'text': ['py', 'txt', 'html', 'css', 'js', 'c', 'md', 'json'],
}


def simple_columns(text_input, num_columns=4):
    max_extension_width = max(map(len, text_input))
    text_table = " "
    for count, item in enumerate(sorted(text_input), 1):
        text_table += item.ljust(max_extension_width+3)
        if count % num_columns == 0 or count == len(text_input):
            text_table += "\n "
    return text_table


SUPPORTED_TYPE_INFO_MESSAGE = '\nThis is the list of currently supported file types for preview:\n\n' \
                              f'{simple_columns(SUPPORTED_TYPES["text"], num_columns=4)}\n' \
                              'Previewing files without extension is not supported.\n' \
                              'You can use the "--preview" argument together with the search ' \
                              'for all files regardless of the extension ("--file-extension ..").\n' \
                              'In this case, the preview will only be displayed for files ' \
                              'with a supported extension.\n\n'

NOT_SUPPORTED_TYPE_MESSAGE = '\nSorry, there is no preview available for this file type.\n' \
                             'You may want to try again without preview.\n' \
                             'This is the list of currently supported file types for preview:\n\n' \
                             f'{simple_columns(SUPPORTED_TYPES["text"], num_columns=4)}\n'


SUPPORTED_PATTERN_MESSAGE = '\nExamples of usage with substitute character "*" ' \
                            'that means "any number of any characters".\n' \
                            'Can be used with: ' \
                            '--path-contains, --filename-contains, --extension-contains\n' \
                            'Help: count-files --args-help find\n' \
                            'Extension starts with substring:\n' \
                            '    count-files --extension-contains substring*\n' \
                            'Filename ends with substring:\n' \
                            '    count-files --filename-contains *substring\n' \
                            'Path contains substring:\n' \
                            '    count-files --path-contains *substring*\n' \
                            '    or simply\n' \
                            '    count-files --path-contains substring\n' \
                            'Search for "*" itself:\n' \
                            '    count-files --path-contains * (starts with "*")\n' \
                            '    count-files --path-contains ** (ends with "*")\n' \
                            '    count-files --path-contains *** (contains one "*")\n' \
                            'Search is case insensitive by default. ' \
                            'You can use the --case-sensitive argument.\n' \
                            'The substring to search for may contain ' \
                            'some special characters inside (sub.str*ing).\n' \
                            'In this case character simply means the character itself.\n' \
                            'Some characters may have special meaning for the terminal. ' \
                            'If the substring to search for contains them or spaces, ' \
                            'you need to specify it in quotes.'

WARNING = '\nPlease use only one of the following commands:\n' \
          'Total number of files.\n' \
          '    count-files --total EXTENSION <arguments>\n' \
          '    Help: count-files --args-help total\n' \
          'File counting by extension.\n' \
          '    count-files <arguments>\n' \
          '    Help: count-files --args-help count\n' \
          'File searching by extension.\n' \
          '    count-files --file-extension FILE_EXTENSION <arguments>\n' \
          '    Help: count-files --args-help search\n' \
          'Find substring in a path, file name or extension.\n' \
          '    count-files --path-contains PATH_SUBSTRING <arguments>\n' \
          '    count-files --filename-contains FILENAME_SUBSTRING <arguments>\n' \
          '    count-files --extension-contains EXTENSION_SUBSTRING <arguments>\n' \
          '    Help: count-files --args-help find\n' \
