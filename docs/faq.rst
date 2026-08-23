Frequently asked questions
==========================

Why does ``rst2html`` work without Pillow, but prezento needs it?
-----------------------------------------------------------------

``rst2html`` (and ``rst2html5``) construct a full docutils settings object
from the stock OptionParser defaults. Image ``:scale:``, ``:width:``, and
``:height:`` then either work (if Pillow is installed) or emit a warning.

prezento uses a **custom HTML5 writer**. Until v1.0.3 the writer did not
pass a complete settings object, so scaled images crashed with
``AttributeError: Values has no attribute file_insertion_enabled``.
That is fixed. Pillow is now a **hard dependency** so ``:scale:`` succeeds
instead of warning.

The warning *“Cannot scale image!  Requires Python Imaging Library.”* is a
docutils **WARNING** (level 2). If ``halt_level`` is too low, the build
exits. prezento keeps halt at error level and installs Pillow so the
warning should not appear in a normal install.

Why does Esbonio fail on my lecture ``.rst`` files?
---------------------------------------------------

`Esbonio <https://github.com/swyddfa/esbonio>`_ is an LSP for **Sphinx
projects**. It expects a ``conf.py``, a Sphinx application, and (in recent
versions) a configured Python environment. Standalone lecture files that
start with ``.. prezento::`` / ``.. slido::`` are not Sphinx documents, so
Esbonio often never finishes initialising.

Use :doc:`tools` — ``tools/slido_ls.py`` — instead. It only needs the RST
text and stdlib Python.

Why is the Geany symbols sidebar empty?
---------------------------------------

Geany’s built-in parser is ctags-based and does not understand ``slido``.
A dedicated ``rst2tags4geany.py`` helper existed briefly and was **removed
in v1.0.3**. Load the LSP plugin and point it at ``slido_ls.py`` (INI
section ``[restructuredtext]``). Then **Restart All Servers**.

The presentation HTML is blank / keys do nothing
------------------------------------------------

The projector file loads ``assets/b6plus.js`` with a **relative** path.
If that file is missing, the HTML still opens but slide mode never starts.

* Copy ``b6plus.js`` next to the HTML (see :doc:`installation`).
* Or rebuild with ``-d outdir`` so prezento copies local assets, including
  ``b6plus.js`` when it can find it.
* Press ``A`` to enter slide mode (b6plus does not start in fullscreen by
  default). Add ``?full`` to the URL to start in slide mode.

``.. yographviz::`` does nothing
--------------------------------

The directive was renamed to ``grafo`` in **v1.1.0**. Update existing
decks. There is no compatibility alias.

What happened to ``substep``?
-----------------------------

v1.1.0 renamed the reveal concept from *substep* to **step**. Mark
incremental content with ``:class: step`` or put ``:step:`` on the
``slido``. Output of ``-s`` is ``*.step4pdf.html`` (not
``*.substep4pdf.html``).

How do I get a PDF?
-------------------

prezento does not embed a PDF engine. Open ``*.concise4pdf.html`` or
``*.step4pdf.html`` in a browser, print, save as PDF. Use **landscape**
and enable **background graphics**. See :doc:`usage`.

Can I still use Hovercraft positioning (``:data-x:``, SVG paths)?
-----------------------------------------------------------------

No. b6plus is a **linear** slide engine. prezento does not implement
impress.js pan/rotate/zoom. If you need a 3-D canvas of slides, keep
using Hovercraft. If you need printable lecture slides with incremental
reveals, prezento is the successor.

Does ``--outdir`` honour ``-s`` / ``-np``?
------------------------------------------

No. ``-d`` / ``--outdir`` always writes ``index.html`` (presentation) and
``<name>.concise4pdf.html`` inside the folder, independently of ``-s`` and
``-np``. Those two flags only control the extra files written **next to
the source**.
