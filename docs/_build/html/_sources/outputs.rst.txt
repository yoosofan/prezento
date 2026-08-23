Output targets
==============

One source file can produce up to three HTML documents plus an optional
standalone folder.

Concise handout (``*.concise4pdf.html``)
----------------------------------------

Flattened document: every incremental item is visible. Optimised for:

* student printouts
* screen readers
* a single-pass PDF

Slides are ``<section class="slide">`` with a slide-number footer.
Full-width CSS is injected so the page is not constrained to a blog
measure.

This is the default ``-o`` target.

Step handout (``*.step4pdf.html``)
----------------------------------

Enabled with ``-s`` / ``--step``.

The engine walks each ``slido`` that contains ``step`` nodes, assigns a
reveal index, and **deep-clones** the slide once per index. Nodes with a
higher index receive ``substep-hidden`` (``opacity: 0``). Printing this
file yields a flip-book: page *k* of a slide matches the projector after
*k* clicks.

Slides without steps are emitted once.

Interactive presentation (``*.presentation.html``)
--------------------------------------------------

b6plus projector mode.

* User CSS from ``:css:`` is linked first (so it can override).
* Full-width and b6plus visibility CSS are appended.
* ``assets/b6plus.js`` is loaded.
* A small boot script calls ``b6plus.init()`` on ``DOMContentLoaded``.
* ``step`` classes are rewritten to ``incremental``.
* ``komento`` blocks become ``section.comment``.

Keyboard (b6plus)
~~~~~~~~~~~~~~~~~

======= ===========================================================
Key     Action
======= ===========================================================
``A``   Enter / leave slide (projection) mode
``Esc`` Leave slide mode
``→``   Next slide or next incremental (also Space)
``←``   Previous
Home    First slide (End = last)
``F``   Fullscreen (also F1)
``2``   Open second window (notes / preview)
``C``   Table of contents (slide mode) or notes (index mode)
``D``   Dark mode (if the stylesheet supports it)
``W``   Draw on the current slide
``?``   List commands
======= ===========================================================

Start in slide mode with ``?full`` on the URL. Jump to a slide with
``#id`` or ``#N``.

These keys come from b6plus, not from prezento. See the
`b6plus documentation <https://www.w3.org/Talks/Tools/b6plus/>`_.

Standalone folder (``-d`` / ``--outdir``)
-----------------------------------------

Creates a directory containing:

* ``index.html`` — same content as ``*.presentation.html``
* ``<name>.concise4pdf.html``
* copies of local images, CSS, JS, and ``b6plus.js`` when found
* ``list_of_resources.rst`` — manifest of copied files

Always generated when ``-d`` is passed, regardless of ``-s`` / ``-np``.
Existing files in the directory are not deleted.

Use this to copy a lecture onto a USB drive or an air-gapped machine.

HTML structure (presentation)
-----------------------------

A compiled slide looks conceptually like::

    <section class="slide t2c" id="paging-hw">
      <h2>Paging Hardware</h2>
      ...
      <div class="slide-number">3</div>
    </section>
    <section class="comment">
      Speaker notes...
    </section>

b6plus treats ``class="slide"`` as a slide boundary and
``class="comment"`` as notes.

CSS injected by prezento
------------------------

* Full-width body/header/footer (all targets).
* ``.substep-hidden { opacity: 0; }`` (step target).
* b6plus rules that hide inactive ``.next`` / ``.incremental > *``
  while ``body.full`` (presentation target).
