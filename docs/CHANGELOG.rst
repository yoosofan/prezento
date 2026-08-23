Changelog
=========

All notable changes to this project are documented here.

The format follows `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_.
The project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

The canonical file in the GitHub repository is ``docs/CHANGELOG.rst``.

Unreleased
----------

**Added**

**Changed**

**Fixed**

**Removed**

v1.1.1 (2026-06-30)
-------------------

* New CLI flag: ``-d`` / ``--outdir DIR`` for a self-contained output
  folder (copied resources, ``index.html``, resource manifest).

v1.1.0 (2026-06-10)
-------------------

**Added**

* ``komento`` directive — private presenter notes for the b6plus
  console (``section.comment``).
* ``step`` class on ``grafo`` SVG so parts of a diagram can appear
  incrementally.

**Changed**

* Renamed the Graphviz directive from ``yographviz`` to ``grafo``.
  Existing slides using ``.. yographviz::`` **must** be updated.
* Improved HTML ``<title>`` handling from the ``prezento`` directive.
* Pillow is a required dependency so image ``:scale:`` / ``:width:`` /
  ``:height:`` work.
* Renamed the reveal concept from *substep* to *step*.

**Fixed**

* docutils settings crashes when scaling images.
* Step expansion for PDF handouts.
* Minor CSS / HTML structure.

**Removed**

* Legacy CSS transforms that existed only as an image-scaling
  workaround.

v1.0.4 (2026-06-08)
-------------------

**Fixed**

* Slide numbering on by default for b6plus presentations. Thanks to
  Bert Bos (W3C), author of b6plus, for the suggestion.

v1.0.3 (2026-06-04)
-------------------

**Added**

* Reference ``assets`` folder under ``tools/``.
* ``slido_ls.py`` LSP server so Kate/Geany can list ``slido`` symbols.

**Fixed**

* ``:scale:`` on the standard ``image`` directive.
* Pillow added to package dependencies.

**Removed**

* ``tools/rst2tags4geany.py``

v1.0.1 (2026-05-31)
-------------------

**Changed**

* Output filenames were renamed in this intermediate release
  (``*.html``, ``*.substep.pdf.html``). Current code (v1.1.x) again uses
  ``*.concise4pdf.html``, ``*.step4pdf.html``, and
  ``*.presentation.html``.
* README and documentation improvements.

**Added**

* Better CLI error handling.

v1.0.0 (2026-05-30)
-------------------

First official release of **prezento**, a rewrite of
``prezentprogramo``.

**Major features**

* Modern docutils (no deprecated APIs)
* ``.. slido::`` (replacing old ``.. slide::``)
* Reveal system via ``:class: substep`` (now ``step``)
* Three output modes: concise HTML, step-expanded HTML, b6plus
  presentation
* ``yographviz`` (now ``grafo``) for Graphviz
* ``src/`` packaging layout
* Custom CSS and JavaScript

**Technical**

* impress.js → **b6plus**
* GPLv3
