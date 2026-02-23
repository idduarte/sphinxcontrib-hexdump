Usage
=====

Enable the extension in ``conf.py``:

.. code-block:: python

   extensions = ["sphinxcontrib.hexdump"]

Basic example:

.. hexdump:: artifacts/sample.any

Bounded example:

.. hexdump:: artifacts/sample.any
   :bytes-per-line: 16
   :start: 0
   :length: 16
   :max-lines: 1

Lowercase example:

.. hexdump:: artifacts/sample.any
   :lowercase:

The directive reads the target in binary mode and does not require any specific file extension.
For large files, use ``:length:`` and/or ``:max-lines:`` to bound generated output.
