Introduction
============

Why text-based slides?
----------------------

GUI slideshow tools (LibreOffice Impress, PowerPoint, Google Slides) make
reorganisation painful. Moving a heading, splitting a list, or inserting a
diagram often means fighting the layout. Lecture notes also need two
artefacts that GUIs rarely produce well at the same time:

* a **live presentation** with incremental reveals
* a **printed handout** that students can annotate

reStructuredText already solves the first problem: content is a tree of
headings, lists, figures, tables, and math. prezento solves the second by
compiling that tree into several HTML targets from one source file.

Why not Hovercraft! or impress.js?
----------------------------------

`Hovercraft! <https://github.com/regebro/hovercraft>`_ pioneered RST →
impress.js presentations. ``prezentprogramo`` forked that idea for
university lectures. impress.js is visually striking, but its 3-D
positioned DOM is a poor match for:

* reliable print / PDF output
* screen readers
* frame-by-frame handouts that mirror live clicks

After years of classroom use, prezento was rewritten around **b6plus**, a
lightweight slide engine maintained with the W3C Talks tools. Slides are
ordinary ``<section class="slide">`` elements. Incremental reveals use
``incremental`` / ``next`` classes. Presenter notes use
``<section class="comment">``.

Design goals
------------

* **Semantic RST authoring** — no hand-written HTML for ordinary slides.
* **Decoupled layers** — static HTML is generated first; b6plus only
  drives the projector mode.
* **Modern docutils** — HTML5 translators, no deprecated APIs
  (requires ``docutils >= 0.21``).
* **Offline first** — no CDN at runtime. Ship ``assets/b6plus.js`` next
  to the HTML.
* **Lecture-grade handouts** — concise and step-expanded HTML that print
  cleanly in landscape with backgrounds enabled.

What prezento is not
--------------------

prezento does **not** implement impress.js pan/rotate/zoom, SVG path
positioning, or Hovercraft templates (XSL). If you need a 3-D canvas of
slides, Hovercraft remains the right tool. If you need linear, printable,
incrementally revealed lecture slides, prezento is the successor.

See :doc:`faq` for migration pitfalls (``yographviz``, Esbonio, missing
``b6plus.js``).

Relationship to other projects
------------------------------

===================== =================================================
Project               Role
===================== =================================================
Hovercraft!           Original RST → impress.js generator (Lennart Regebro)
prezentprogramo       Earlier fork used for lectures; now in limited maintenance
prezento              Successor: b6plus, latest docutils, extra directives
b6plus                Runtime slide engine (Bert Bos / W3C Talks)
docutils              RST parser and HTML5 writer
===================== =================================================

License
-------

prezento is licensed under the **GNU GPL v3.0 or later**.
