Making presentations
====================

A note on terminology
---------------------

Hovercraft and impress.js use *slide* and *step* almost interchangeably.
prezento keeps them distinct:

* A **slide** is one ``.. slido::`` block — one projector page.
* A **step** (formerly *substep*) is an incremental reveal *inside* a
  slide. In the source you mark it with ``:class: step``, or with the
  ``:step:`` flag on the ``slido``. In b6plus output this becomes the
  ``incremental`` class.

File structure
--------------

A presentation is a normal ``.rst`` file. It **must** start with the
``prezento`` directive (global metadata), then one or more four-space
indented ``slido`` blocks.

.. code-block:: rst

   .. prezento:: Operating Systems — Paging (By Ahmad Yoosofan)
      :css: ./assets/style.css

   .. slido:: Introduction to Paging
      :id: slide-paging-intro

      Paging eliminates external fragmentation by dividing physical
      memory into fixed-size **frames**.

      * Page size equals frame size.
      * The OS tracks free frames.

   .. slido:: The TLB
      :class: t2c

      The TLB caches recent virtual-to-physical translations.

      #. CPU generates a logical address.
      #. The page number is looked up in the TLB.
      #. A **hit** returns the frame immediately.
      #. A **miss** walks the page table in RAM.

Indentation
~~~~~~~~~~~

All content that belongs to a slide must be indented (conventionally
four spaces) under ``.. slido::``. Unindented material is not part of
that slide.

This is the main syntactic difference from Hovercraft, which uses a
transition marker (``----``) between heading-delimited slides.

reStructuredText you already know
---------------------------------

Headings, emphasis, lists, tables, images, math, and code work as in
any RST document.

**Emphasis**::

    *italic* and **bold**

**Bullet and numbered lists**::

    * Frame
    * Page

    #. Translate
    #. Access memory

**Images** (Pillow is required for ``:scale:``)::

    .. image:: os/img/memory/paging_model.png
       :align: center
       :scale: 110%
       :height: 300px

**Math** (docutils math; style with CSS / MathJax in your theme)::

    .. math::

       EAT = h \times (t_{TLB} + t_{mem})
           + (1 - h) \times (t_{TLB} + 2 t_{mem})

**Code**::

    .. code:: python

       def physical(frame, offset):
           return (frame << n) | offset

**CSV tables**::

    .. csv-table::
       :header-rows: 1

       page,frame
       0,2
       1,5

Roles such as ``:math:``, custom ``:rtl:`` / ``:ltr:`` (if you define
them), and standard hyperlinks are passed through to HTML.

Incremental reveals (steps)
---------------------------

Mark a container or an element with class ``step``.

Reveal a whole list item by item:

.. code-block:: rst

   .. slido:: Address bits

      .. class:: step

         #. Address width = log2(maximum memory)
         #. Offset bits *d* = log2(page size)
         #. Page bits *p* = address width − *d*

Reveal a math block after the setup text:

.. code-block:: rst

   .. class:: step

      * :math:`t_t = 1` ns, :math:`h_t = 0.95`

   .. math::
      :class: step

      table = 0.95 \times 1 + 0.05 \times 101 = 6

On a ``slido`` that itself has the ``:step:`` flag (or class ``step``),
each child of the slide (except titles) is treated as a successive
incremental.

How it is compiled
~~~~~~~~~~~~~~~~~~

* **Presentation HTML** — ``_b6_transform`` maps ``step`` to b6plus
  ``incremental``. During the talk, Space / → reveals the next child.
* **Step HTML** (``-s``) — the AST is cloned once per reveal index.
  Later items get ``substep-hidden`` so each printed page matches one
  click.
* **Concise HTML** — every item is visible; classes used only for
  styling.

Presenter notes
---------------

Use ``komento`` (Esperanto for *comment*). Notes are wrapped as
``<section class="comment">`` in the presentation target. b6plus hides
them on the projector and shows them in the second window (press
``2``).

.. code-block:: rst

   .. slido:: Addressing Hardware

      * Page offset (d)
      * Page number (p)

      .. komento::

         Write the formula *m − n* on the board before the next slide.

This replaces Hovercraft’s ``.. note::`` for speaker notes. The
standard docutils ``note`` admonition is left alone (it still renders
as a visible note box).

External files
--------------

Images referenced by relative path should sit next to the RST (or in a
subdirectory). With ``--outdir``, prezento copies local images, CSS, JS,
and ``b6plus.js`` it can discover into the output folder.

Absolute URLs are left as-is and are **not** copied.

Adding JavaScript
-----------------

Pass scripts in the ``prezento`` directive:

.. code-block:: rst

   .. prezento:: Course title
      :css: ./assets/style.css
      :js: ./assets/custom.js, ./assets/mathjax/tex-chtml.js

Each path becomes a ``<script src>`` in the generated HTML. There is no
separate header/body split (Hovercraft’s ``:js-header:`` / ``:js-body:``).
Keep scripts local for air-gapped halls.

Portable presentations
----------------------

Generated HTML is ordinary HTML5. Any modern browser can show it —
including a borrowed conference laptop — **if** the assets travel with
the files.

The reliable way to pack a lecture is::

    prezento os.paging.rst -s -d dist/os-paging

That folder contains ``index.html`` (the projector deck), the concise
handout, copied local resources, and ``list_of_resources.rst``. Copy the
folder to a USB stick. Do not rely on Google Fonts or a CDN.

For fonts, define ``@font-face`` in your CSS and keep the font files
under ``assets/fonts/``. See :doc:`styling`.

Naming convention (slide repository)
------------------------------------

In https://github.com/yoosofan/slide new decks live at the repository
root as::

    <course_abbreviation>.<topic>.rst

Examples: ``os.paging.rst``, ``db.sql2.rst``.
