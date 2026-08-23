Custom directives
=================

prezento registers four RST directives on import of ``prezento.main``.

``prezento``
------------

Document-level configuration. Place it **once**, near the top of the
file. It produces no visible node; options are stored on
``document.presentation_config``.

.. code-block:: rst

   .. prezento:: Operating Systems - Paging (By Ahmad Yoosofan)
      :css: ./assets/style.css, ./assets/print.css
      :js: ./assets/custom.js
      :width: 1280
      :height: 720

**Arguments**
    Optional title. Becomes the HTML ``<title>`` (and often the first
    heading context). Whitespace in the title is allowed.

**Options**

============= ========================================================
Option        Meaning
============= ========================================================
``:css:``     Comma-separated stylesheet URLs, injected as
              ``<link rel="stylesheet">``.
``:js:``      Comma-separated script URLs, injected as
              ``<script src>``.
``:width:``   Hint for slide geometry (passed through config).
``:height:``  Hint for slide geometry (passed through config).
============= ========================================================

``slido``
---------

Hard boundary for one slide. Content **must** be indented.

.. code-block:: rst

   .. slido:: Paging Hardware
      :id: paging-hw
      :class: t2c step

      .. image:: os/img/memory/paging_hardware.png
         :align: center
         :height: 320px

**Arguments**
    Optional slide title, rendered as ``<h2>`` inside
    ``<section class="slide">``.

**Options**

============= ========================================================
Option        Meaning
============= ========================================================
``:id:``      HTML id on the ``<section>``. Stable CSS/JS hooks.
``:class:``   Extra classes on the section (layout helpers such as
              ``t2c``, ``n2c``, plus ``step`` for incremental children).
``:step:``    Flag. Treat children of the slide as successive
              incrementals (same idea as putting class ``step`` on the
              slido).
============= ========================================================

Empty title
~~~~~~~~~~~

``.. slido::`` with no argument is valid (title-less figure slides).
The LSP still lists them as numbered untitled slides.

``grafo``
---------

Embed Graphviz DOT as inline SVG. Replaces the old name
``yographviz`` (v1.1.0). Update existing decks; there is no alias.

.. code-block:: rst

   .. grafo::
      :align: center
      :width: 1700px
      :class: diagram

      digraph PagingHW {
          rankdir=LR;
          CPU -> Logical [label="Generates"];
          Logical -> PageTable [label="Index"];
          PageTable -> Physical [label="Frame"];
      }

**Options**

============= ========================================================
Option        Meaning
============= ========================================================
``:align:``   ``left``, ``center`` (default), or ``right``.
``:class:``   Extra classes on the wrapping ``div.graphviz-container``.
``:width:``   Written onto the ``<svg>`` (Graphviz ``pt`` size is
              stripped so CSS can win).
``:height:``  Same for height.
``:scale:``   Scale factor for the SVG (where supported).
``:alt:``     Alternate text.
``:name:``    Name / identifier.
``:target:``  Optional link target.
============= ========================================================

DOT edges or nodes may carry ``class="step"`` so parts of the diagram
appear incrementally in b6plus (rewritten to ``incremental``).

The Graphviz CLI must be installed. Failures yield an empty SVG rather
than aborting the whole build.

``komento``
-----------

Speaker-only notes (v1.1.0).

.. code-block:: rst

   .. komento::
      :class: aside
      :id: note-tlb

      Remind them that TLB is *not* a data cache.

Rendered as ``<section class="comment">`` in presentation HTML. b6plus
shows this in the notes / second window, not on the projector.

**Options:** ``:class:``, ``:id:``.

Standard docutils directives
----------------------------

Everything else is ordinary docutils: ``image``, ``figure``, ``math``,
``code``, ``csv-table``, ``container``, ``class``, ``raw``, ``include``,
``role``, etc.

Image scaling requires Pillow. Without it, docutils warns
“Cannot scale image! Requires Python Imaging Library.” prezento lists
Pillow as a hard dependency so ``:scale:`` works.

Migration notes
---------------

* ``.. yographviz::`` → ``.. grafo::``
* class ``substep`` → ``step`` (current ``_b6_transform`` looks for
  ``step``)
* Hovercraft ``----`` slide separators are **not** used. Use
  ``.. slido::``.
* Hovercraft ``.. note::`` presenter notes → ``.. komento::``
  (``note`` remains the standard admonition).
* Hovercraft ``:data-x:`` / SVG path positioning has no equivalent.
