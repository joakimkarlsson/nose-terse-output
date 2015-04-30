=================
nose-terse-output
=================

Really terse output from your nose tests. Just the bare essentials.

Nose-terse-output is inspired by nose-machineout. It's a reporter plugin to nose that doesn't produce any output if a nose test run is successful, and only produce one line per error in a format that is easily parseable by editors, like VIM.

Default output from a failing test run:

.. code:: bash

   $ nosetests --with-terseout
   path/to/test.py:123 test name: 'foo' != 'bar'

To get a compact print out of the stack as well:

.. code:: bash

   $ nosetests --with-terseout --print-stack

Install with:

.. code:: bash

    $ pip install nose-terse-output
