================================
CHANGELOG for prezento
================================

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Unreleased]
============

**Added**

**Changed**

**Fixed**

**Removed**


v1.1.0 (2026-06-10)
===================

**Added**

* ``komento`` directive — allows private presenter notes (speaker comments) that appear only in the b6plus presentation console.
* step can be added as class in grafo svg image for step bt step showing parts of corresponding generated svg image.

**Changed**

* Renamed the Graphviz directive from ``yographviz`` to ``grafo`` (more intuitive and shorter name).
  * **Note**: Existing slides using ``.. yographviz::`` must be updated to ``.. grafo::``.
* Improved title handling in HTML output based on the ``prezento`` directive.
* Made Pillow (PIL) a required dependency to properly support the ``:scale:``, ``:width:``, and ``:height:`` options on images.
* Renamed the substep to step

**Fixed**

* Various docutils settings issues that caused crashes when using image scaling attributes.
* Better handling of substep expansion for PDF handouts.
* Minor CSS and HTML structure improvements for cleaner output.

**Removed**

* Legacy CSS transformations that were previously needed as a workaround for image scaling.

v1.0.4 (2026-06-08)
===================

**Fixed**

* Enabled slide numbering by default for presentations utilizing the B6+ framework, eliminating the need for manual workarounds or alternative implementation methods. Special thanks to Bert Bos (W3C), creator and maintainer of B6+, for this excellent suggestion.

v1.0.3 (2026-06-04)
===================

**Added**

* asstes folder added to the tools folder of the repository for reference
* `slido_ls.py` LSP server add to help Kate/Geany IDE to show symbols of `slido`

**Fixed**

* scale attribute for image directive is added
* pillow is added to the package dependencies

**Removed**

* tools/rst2tags4geany.py

v1.0.1 (2026-05-31)
===================

**Changed**

* Renamed output files for better clarity:
    - ``*.concise4pdf.html`` → ``*.html`` (standard version)
    - ``*.substep4pdf.html`` → ``*.substep.pdf.html``
* Improved README.rst and project documentation
* Minor code cleanup and bug fixes

**Added**

* Better error handling and user feedback in CLI


v1.0.0 (2026-05-30)
===================

**Initial Release**

This is the first official release of **prezento** — a modern rewrite of the previous `prezentprogramo` tool.

**Major Features**

* Full support for modern docutils (no deprecated APIs)
* New ``.. slido::`` directive (replacing old ``.. slide::``)
* Powerful and flexible **substep** system using ``:class: substep``
* Three output modes:
    * Standard HTML (for PDF printing)
    * Substep-expanded HTML (step-by-step handouts)
    * b6plus presentation mode (interactive slides)
* ``yographviz`` directive for embedded Graphviz diagrams
* Proper package structure using ``src/`` layout
* Support for custom CSS and JavaScript

**Technical Improvements**

* Switched from impress.js to **b6plus**
* Cleaner architecture and better code organization
* Migration tools for old slides
* Proper asset handling (``assets/`` folder)

**Project Structure**

* Adopted modern Python packaging standards (`pyproject.toml` + `src/` layout)
* Added comprehensive README.rst and documentation

**License**

* Changed to **GPLv3**
