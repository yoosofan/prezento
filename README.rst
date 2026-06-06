======================================
prezento — Modern RST Slide Generator
======================================

**prezento** is a powerful, offline-first slide generator that converts reStructuredText (RST) files into beautiful, interactive HTML presentations.

It is a complete rewrite of `prezentprogramo` (a former fork of Hovercraft) with modern architecture, improved substep handling, and a switch from impress.js to `b6plus <https://www.w3.org/Talks/Tools/b6plus/>`_.

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: LICENSE

.. contents:: Table of Contents
   :depth: 2

Features
========

* Clean and semantic RST-based slide authoring
* Powerful **substep / incremental reveal** system with fine-grained control
* Multiple output formats:
   * Standard HTML (for direct PDF printing)
   * Substep-expanded HTML (step-by-step handouts)
   * b6plus presentation mode (for projectors / live talks)
* Embedded Graphviz diagram support (`yographviz` directive)
* Full offline capability
* Custom CSS and JavaScript support
* High-quality print/PDF output

Why prezento?
=============

The original `prezentprogramo` was heavily tied to impress.js and had complex structure. After years of use, I decided to rewrite it from scratch with the following goals:

* Better substep semantics for lecture note substeps(Showing content of a page gradually)
* Modern docutils usage (no deprecated APIs)
* Cleaner code architecture
* Switch to **b6plus** — a lightweight and actively maintained presentation library
* Easier maintenance and future extensibility

This version is **not compatible** with original Hovercraft or prezentprogramo RST files, but it offers a much better authoring experience.

Sample Slides
=============

You can see real-world examples of prezento in use here:

https://github.com/yoosofan/slide

Assets Requirement
==================

The generated HTML slides require the following asset:

* ``assets/b6plus.js``: b6plus javasrcript library for on screen presentation

**Important**: After generating HTML files, you must have an ``assets/`` folder next to them containing this file.

These assets are taken from the `b6plus <https://www.w3.org/Talks/Tools/b6plus/slides.zip>`_ project. You can update them whenever a newer version is released.

You can download them from `my slides <https://github.com/yoosofan/slide/tree/main/assets>`_ too.

Installation
============

.. code:: sh

    pip install prezento

From source (recommended during early development):

.. code-block:: bash

    git clone https://github.com/yoosofan/prezento.git
    cd prezento
    pip install -e .

Usage
=====

Basic usage:

.. code-block:: bash

    prezento your_slides.rst

This will generate two output files in the same directory:

* ``your_slides.concise4pdf.html`` — Standard version (good for printing)
* ``your_slides.presentation.html`` — b6plus interactive version

Options:

.. code-block:: bash

    prezento input.rst -o output.html
    prezento input.rst -s               # Generate ``your_slides.substep4pdf.html`` — Step-by-step version
    prezento input.rst -np              # Skip b6plus version for screen presentation

Project Structure (Development)
===============================

.. code-block:: text

    prezento/
    ├── src/
    │   └── prezento/
    │       ├── __init__.py
    │       └── main.py
    ├── docs/
    │   └── CHANGELOG.rst
    └── tools/
        ├── readme.rst
        ├── slido_ls.py
        ├── build.sh
        └── clean.sh

Contributing
============

Contributions are welcome! This project is still in active development.

If you want to help, please:

* Open an issue for bugs or feature requests
* Submit pull requests for improvements
* Test with complex slide decks

License
=======

This project is licensed under the **GNU General Public License v3.0** (GPLv3).

See the `LICENSE` file for the full license text.

You are free to use, modify, and distribute this software under the terms of GPLv3.

Acknowledgments
===============

* Inspired by `Hovercraft <https://github.com/regebro/hovercraft>`_ and the original `prezentprogramo <https://github.com/yoosofan/prezentprogramo>`_
* Uses `b6plus <https://www.w3.org/Talks/Tools/b6plus/>`_ for presentation mode. https://www.w3.org/Talks/Tools/b6plus/slides.zip
* Built on top of `docutils <https://docutils.sourceforge.io/>`_

Author
======

**Ahmad Yoosofan**

- GitHub: https://github.com/yoosofan
- Slides: https://github.com/yoosofan/slide
