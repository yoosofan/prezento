Using prezento
==============

Basic invocation
----------------

.. code-block:: bash

   prezento your_slides.rst

By default this writes two files in the same directory as the source:

* ``your_slides.concise4pdf.html`` — all content visible (print / PDF)
* ``your_slides.presentation.html`` — b6plus interactive deck

Command line
------------

.. code-block:: text

   prezento [-h] [-o OUTPUT] [-s] [-np] [-d DIR] input_file

Positional arguments
~~~~~~~~~~~~~~~~~~~~

``input_file``
    Path to the reStructuredText presentation.

Optional arguments
~~~~~~~~~~~~~~~~~~

``-h``, ``--help``
    Show help and exit.

``-o OUTPUT``, ``--output OUTPUT``
    Filename for the concise HTML. Defaults to
    ``<basename>.concise4pdf.html``.

``-s``, ``--step``
    Also write ``<basename>.step4pdf.html``: each incremental reveal
    becomes its own cloned slide for flip-book PDF printing.

``-np``, ``--no-presentation``
    Skip ``<basename>.presentation.html``.

``-d DIR``, ``--outdir DIR``
    Build a self-contained directory: ``index.html`` (same content as
    the presentation HTML), ``<name>.concise4pdf.html``, copies of
    local images/CSS/JS/``b6plus.js`` when found, and a
    ``list_of_resources.rst`` manifest.

    This folder is generated **independently** of ``-s`` and ``-np``.
    Those flags only control the extra files written next to the
    source. ``--outdir`` does not delete pre-existing files in ``DIR``.

Examples
--------

Generate everything including the step handout::

    prezento os.paging.rst -s

Custom concise filename, no projector file::

    prezento os.paging.rst -o handout.html --no-presentation

Pack a portable folder for a USB stick::

    prezento os.paging.rst -s -d dist/os-paging

Convert to PDF
--------------

prezento does not embed a PDF engine. Open the concise (or step) HTML in
a browser and print:

1. Open ``*.concise4pdf.html`` (or ``*.step4pdf.html``).
2. Print → Save as PDF.
3. Use **landscape** orientation.
4. Enable **background graphics** so slide colours and diagrams print.

The step HTML is a long sequence of pages: one printed page per reveal
state, matching what the audience saw after each click.

Python API
----------

.. code-block:: python

   from prezento.main import publish_to_html

   html_bytes = publish_to_html(source_rst, output_type="standard")
   # output_type: "standard" | "step" | "presentation"

``publish_to_html`` returns encoded HTML (``bytes``).

Typical lecture workflow
------------------------

1. Author ``course.topic.rst`` with ``.. prezento::`` and ``.. slido::``.
2. Run ``prezento course.topic.rst -s``.
3. Rehearse ``course.topic.presentation.html`` in a browser (press
   ``A`` to enter slide mode — see :doc:`outputs`).
4. Print ``course.topic.concise4pdf.html`` for students, or the step
   file if you want a click-accurate handout.
