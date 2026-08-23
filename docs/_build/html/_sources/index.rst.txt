.. prezento documentation master file.

prezento — Modern RST Slide Generator
=====================================

**prezento** converts reStructuredText into interactive HTML presentations
and print-ready educational handouts. It is a complete rewrite of
``prezentprogramo`` (itself a fork of Hovercraft!) and uses the W3C
`b6plus <https://www.w3.org/Talks/Tools/b6plus/>`_ framework instead of
impress.js.

Write slides in plain text. Generate a live projector deck, a concise
printable handout, and a frame-by-frame step handout from the same source.

.. code-block:: bash

   pip install prezento
   prezento lecture.rst

This produces:

* ``lecture.concise4pdf.html`` — flattened handout, ready to print
* ``lecture.presentation.html`` — interactive b6plus slideshow

Add ``-s`` for a step-expanded PDF handout, or ``-d outdir`` for a
self-contained folder with copied assets.

.. note::

   This documentation is a Sphinx project intended for
   `Read the Docs <https://readthedocs.io>`_, following the same layout as
   `Hovercraft! <https://hovercraft.readthedocs.io>`_
   (``conf.py``, ``index.rst``, a ``toctree`` of topic files, ``Makefile``).

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User guide

   introduction
   installation
   usage
   presentations
   directives
   outputs
   styling

.. toctree::
   :maxdepth: 2
   :caption: Extra

   tools
   examples
   faq
   contributing
   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
