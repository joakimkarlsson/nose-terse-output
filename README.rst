=================
nose-terse-output
=================

Really terse output from your nose tests. Just the bare essentials.

Nose-terse-output is inspired by nose-machineout_. It's a reporter plugin to nose that doesn't produce any output if a nose test run is successful, and only produce one line per error in a format that is easily parseable by editors, like VIM.

Nose's error messages are really hard for tools, like text editors, to parse in order to navigate to the location of the error. nose-terse-output takes that output and parses it to produce one line of information per failed test. That line has the format:

.. code:: bash

   <path>:<line> <error message>

That's a whole lot easier for a text editor to parse.

nose-terse-output accomplishes this by starting at the bottom of the call stack for the error, and walk upwards until it finds the first location that looks interesting.

By default, the first stack frame that comes from the same basepath as the current directory and that doesn't match 'python' or 'venv' will be selected as the location of the failing test.

You can change the patterns of paths to ignore when walking the stack with the `--terse-ignore` argument. You can use `--terse-ignore` several times. You can also tell nose-terse-output that it's ok to consider non local directories by using the `--terse-outside-local` argument.

Default output from a failing test run:

.. code:: bash

   $ nosetests --with-terseout
   path/to/test.py:123 test name: 'foo' != 'bar'

To get a compact print out of the stack as well:

.. code:: bash

   $ nosetests --with-terseout --print-stack


To supply your own directories you'd like to ignore:

.. code:: bash

   $ nosetests --with-terseout --terse-ignore="venv" --terse-ignore="helpers"


To consider non-local directories:

.. code:: bash

   $ nosetests --with-terseout --terse-outside-local

Install with:

.. code:: bash

    $ pip install nose-terse-output


.. _nose-machineout: https://pypi.python.org/pypi/nose_machineout
