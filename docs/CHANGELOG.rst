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
