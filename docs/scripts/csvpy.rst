=====
csvpy
=====

Description
===========

Loads a CSV file into a :class:`agate.csv.Reader` object and then drops into a Python shell so the user can inspect the data however they see fit:

.. code-block:: none

   usage: csvpy [-h] [-d DELIMITER] [-t] [-q QUOTECHAR] [-u {0,1,2,3}] [-b]
                [-p ESCAPECHAR] [-z FIELD_SIZE_LIMIT] [-e ENCODING] [-L LOCALE]
                [-S] [--blanks] [--null-value NULL_VALUES [NULL_VALUES ...]]
                [--date-format DATE_FORMAT] [--datetime-format DATETIME_FORMAT]
                [-H] [-K SKIP_LINES] [-v] [-l] [--zero] [-V] [--dict] [--agate]
                [FILE]

   Load a CSV file into a CSV reader and then drop into a Python shell.

   positional arguments:
     FILE                  The CSV file to operate on. If omitted, will accept
                           input as piped data via STDIN.

   optional arguments:
     -h, --help            show this help message and exit
     --dict                Load the CSV file into a DictReader.
     --agate               Load the CSV file into an agate table.

This tool will automatically use the IPython shell if it is installed, otherwise it will use the running Python shell.

.. note::

    Due to platform limitations, csvpy does not accept file input as piped data via STDIN. 

See also: :doc:`../common_arguments`.

Examples
========

Basic use:

.. code-block:: console

$ csvpy examples/dummy.csv
   Welcome! "examples/dummy.csv" has been loaded in a reader object named "reader".
   >>> next(reader)
   ['a', 'b', 'c']

As a dictionary:

.. code-block:: console

   $ csvpy --dict examples/dummy.csv
   Welcome! "examples/dummy.csv" has been loaded in a DictReader object named "reader".
   >>> next(reader)
   {'a': '1', 'c': '3', 'b': '2'}

As an agate table:

.. code-block:: console

   $ csvpy --agate examples/dummy.csv
   Welcome! "examples/dummy.csv" has been loaded in a from_csv object named "reader".
   >>> reader.print_table()
   |    a | b | c |
   | ---- | - | - |
   | True | 2 | 3 |
