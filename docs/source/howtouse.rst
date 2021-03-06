How to use
----------


CLI arguments
^^^^^^^^^^^^^

Arguments can be specified in both short and long form. For example: ``-a`` or ``--all``.
::

   usage: count-files [-h] [-hc]
                      [-v] [-st]
                      [-a] [-c]
                      [-nr] [-nf]
                      [-alpha]
                      [-t EXTENSION]
                      [-sf] [-ts]
                      [-fe FILE_EXTENSION]
                      [-fm PATTERN][-fs]
                      [-p] [-ps PREVIEW_SIZE]
                      [path]


   usage: count-files [--help] [--help-cmd]
                      [--version] [--supported-types]
                      [--all] [--case-sensitive]
                      [--no-recursion] [--no-feedback]
                      [--sort-alpha]
                      [--total EXTENSION]
                      [--show-folders] [--total-size]
                      [--file-extension FILE_EXTENSION]
                      [--filename-match PATTERN] [--file-sizes]
                      [--preview] [--preview-size PREVIEW_SIZE]
                      [path]

Common arguments
""""""""""""""""

``path``, ``--all``, ``--case-sensitive``, ``--no-recursion``, ``--no-feedback``

Special arguments
"""""""""""""""""

* File counting by extension (sorted table):
   ``--sort-alpha``

* File searching by extension (list with file paths):
   ``--file-extension``, ``--file-sizes``, ``--preview``, ``--preview-size``

* File searching by pattern (list with file paths):
   ``--filename-match``, ``--file-sizes``, ``--preview``, ``--preview-size``

* Total number of files (number):
   ``--total``, ``--show-folders``, ``--total-size``

Getting help
^^^^^^^^^^^^

To check the list of available options and their usage, you just need to use
one of the following commands::

   count-files -h

   count-files --help

Search in help by topic - argument or group name(count, search, total)::

   count-files -hc
   
   count-files --help-cmd

Check the version number of the program::

   count-files -v
   
   count-files --version

Get the list of currently supported file types for preview::

   count-files -st
   
   count-files --supported-types

.. _path-label:

The ``path`` argument
^^^^^^^^^^^^^^^^^^^^^

Optionally, you can pass it a path to the directory to scan. If you prefer, you
can leave that argument empty, and it will scan the current working directory.

To process files in the user's home directory, you can use ``~`` (tilde).

If there are spaces in the folder names, then ``path`` should be specified in
quotation marks. For example, in Windows: ``count-files "~\Desktop\New folder"``

.. _non-recursive-label:

Non-recursive search or counting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The optional ``-nr`` or ``--no-recursion`` switch argument tells the
application not to scan recursively through the subdirectories.

.. _hidden-label:

Hidden files and directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For supported operating systems (Linux, macOS, iOS, Windows), any hidden files or folders are ignored by default. But you can add the ``-a`` or ``--all`` optional
switch argument to make it count or search for all files.

For other operating systems in which Python can be run, this option to include/exclude hidden files is not available. And as a result, all existing files will be included.

In Windows, files and directories considered hidden by this application are
those for which the ``FILE_ATTRIBUTE_HIDDEN`` attribute is set to true.

In Linux, macOS, iOS and other Unix-like operating systems, a file or
directory is considered to be hidden if its name starts with a ``.`` (dot).


.. _case-sensitivity-label:

Case sensitivity
^^^^^^^^^^^^^^^^

The names of extensions are case insensitive by default. The results for
``ini`` and ``INI`` will be the same. To distinguish between similar
extensions in different cases, use the ``-c`` or ``--case-sensitive`` switch
argument.

* File counting by extension (sorted table):

   In this case, the file extensions in the table will be displayed as is (in
   lowercase and uppercase).

* File searching by extension (using ``-fe`` or ``--file-extension``):

   The result of the search will be a list with paths to files with an extension in the corresponding register.

* File searching by pattern (using ``-fm`` or ``--filename-match``):

   The search result will be a list of file paths with file names that exactly match the case-sensitive pattern.

* Total number of files (using ``-t`` or ``--total``):

   For total counting of files with a specific extension, this option is also
   available. The result of the counting will be a total number of files with an extension in the corresponding register.

.. _feedback-label:

Customizing operation feedback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the program displays an operating indicator that consists in
successively printing processed file names in a single line. File names are
not displayed, however, when searching for a particular extension, if there
are no such files in the folder or if the files are hidden, and the
argument ``--all`` was not specified.

This kind of feedback is available by default when counting files by extension
and when counting the total number of files (using ``-t`` or ``--total``). The
optional ``-nf`` or ``--no-feedback`` switch argument disables it.

Using the ``--no-feedback`` argument allows you to speed up a little the
processing of a large amount of files/folders.

When searching for files by extension or by pattern(using ``--file-extension`` or ``--filename-match``) the feedback mechanism is the list of file paths itself.

File counting by extension
^^^^^^^^^^^^^^^^^^^^^^^^^^

To count all files by extension, you can simply use the command
``count-files`` and, if necessary, specify one or more of the common
arguments: ``path``, ``--all``, ``case-sensitive``, ``--no-recursion``,
``--no-feedback``. You can sort the extensions in the table alphabetically using the ``--sort-alpha`` argument.

Example: ``count-files``

.. seealso:: :ref:`count-label`

The ``--sort-alpha`` argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, result of file counting by extension is a table that lists all the
file extensions found and displays the frequency for each file extension. To
sort the extensions alphabetically, use the ``-alpha`` or ``--sort-alpha``
argument.

Example: ``count-files --sort-alpha``

File searching by extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another main feature of this application consists in searching files by a
given extension, which presents to the user a list of all found files.

Using ``-fe`` or ``--file-extension`` argument, you can find all the files
that have the specified extension. You can get additional information about the size of each found file and see a short preview for text files (``--file-sizes``, ``--preview``, ``--preview-size`` optional arguments).

If necessary, specify one or more of the common
arguments: ``path``, ``--all``, ``case-sensitive``, ``--no-recursion``.

Example: ``count-files --file-extension txt``

.. seealso:: :ref:`search-label`

File searching by pattern
^^^^^^^^^^^^^^^^^^^^^^^^^

You can also search for files using Unix shell-style wildcards: ``*``, ``?``, ``[seq]``, ``[!seq]`` (with ``-fm`` or ``--filename-match`` argument).
``*`` - matches everything (zero or more occurrences of any character), ``?`` - matches any single character,
``[seq]`` - matches any character in seq, ``[!seq]`` - matches any character not in seq.

Some optional arguments are also available (``--file-sizes``, ``--preview``, ``--preview-size`` arguments). If necessary, specify one or more of the common
arguments: ``path``, ``--all``, ``case-sensitive``, ``--no-recursion``.

Example: ``count-files --filename-match *.????``

.. seealso:: :ref:`pattern-label`

Total counting of files
^^^^^^^^^^^^^^^^^^^^^^^

To count the total number of files, the number of files with a specific
extension or the number of files without any extension you can use the ``-t``
or ``--total`` argument and specify the name of the extension.

You can also get a list of folders in which the found files are located, the number of found files in each folder and the total combined size of these files (``--show-folders`` and ``--total-size`` optional arguments). 
When recursively counting all files(``--total ..``) and using the ``--show-folders`` argument, all folders containing files are displayed.

If necessary, specify one or more of the common
arguments: ``path``, ``--all``, ``case-sensitive``, ``--no-recursion``,
``--no-feedback``.

Example: ``count-files --total json``

.. seealso:: :ref:`total-label`

Preview text files
^^^^^^^^^^^^^^^^^^

Preview is available as an option when searching files using the ``--filename-match`` or
``--file-extension`` arguments.

The default text preview size depends on the terminal width settings. You can
change this value by specifying the argument ``-ps`` or ``--preview-size``
followed by an integer (the number of characters to display from each file).

Example: ``count-files --file-extension css --preview --preview-size 50``

File sizes
^^^^^^^^^^

You can get additional information about the size of each file using the
``-fs`` or ``--file-sizes`` argument. This option is only available when
searching files using the ``--filename-match`` or ``--file-extension`` arguments.

Example: ``count-files --file-extension js --file-sizes``

When counting the total number of files (using ``--total`` argument) you can also get the total combined size of found files.

Example: ``count-files --total py --total-size``
