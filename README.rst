======================================
prezento — Modern RST Slide Generator
======================================

**prezento** is an advanced, offline-first slide generator designed to convert standard reStructuredText (RST) documents into highly semantic, interactive HTML presentations and print-ready educational handouts.

Born out of the necessity for robust lecture material generation, `prezento` is a complete architectural rewrite of `prezentprogramo` (a historical fork of Hovercraft). It features a modern Python rendering pipeline, a highly engineered incremental-reveal (step) system, and a core transition to the standard-compliant `b6plus <https://www.w3.org/Talks/Tools/b6plus/>`_ presentation framework.

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: LICENSE

.. contents:: Table of Contents
   :depth: 2

Features
========

* **Semantic RST Authoring:** Define slides using clean, human-readable structural text without manual HTML/DOM manipulation.
* **Granular Step-by-Step Expansion:** A mathematically precise AST (Abstract Syntax Tree) unrolling engine that creates perfect frame-by-frame PDF handouts mirroring your live presentation clicks.
* **Native Graphviz Integration:** Embed complex architecture diagrams directly in your slides using the custom ``grafo`` directive, with automated SVG sanitization and CSS scaling.
* **Presenter Console Support:** Private speaker notes injected seamlessly into the `b6plus` presenter dashboard via the ``komento`` directive.
* **Offline-First Architecture:** Zero runtime reliance on external CDNs or APIs. Presentations render flawlessly in air-gapped environments or low-connectivity lecture halls.
* **Multi-Format Generation:** Simultaneously compiles your single source text into a live presentation, a flat summary document, and a frame-by-frame handout.

Why prezento?
=============

The original `prezentprogramo` relied heavily on `impress.js`. While visually impressive, `impress.js` introduced immense structural DOM complexities that made generating clean, static PDF handouts highly problematic. After years of field-testing in university lecture settings, `prezento` was redesigned from scratch to solve these fundamental limitations:

* **Strict Decoupling:** Complete separation of the static layout generation from the interactive JavaScript presentation layer.
* **Modernized Docutils Pipeline:** Eradication of legacy Docutils hooks in favor of clean, isolated HTML5 tree translators and native node visiting.
* **Framework Migration:** Transitioning to **b6plus**, an elegant, lightweight presentation package maintained by the W3C presentation community, which handles progressive reveals (`incremental` classes) and hierarchical lists far more gracefully.

Sample Slides
=============

Real-world examples of prezento in use are located here:

https://github.com/yoosofan/slide

The following samples shows more details for learning and using prezento.

Sample 1
--------
* `rst input source <https://github.com/yoosofan/slide/blob/main/os.paging.rst>`_
    * `download <http://yoosofan.github.io/slide/os.paging.rst>`_
* `prezentation output html <https://yoosofan.github.io/slide/os.paging.presentation.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/os.paging.presentation.html>`_
* `output of concise html for pdf <https://yoosofan.github.io/slide/os.paging.concise4pdf.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/os.paging.concise4pdf.html>`_
* `output of step html for pdf <https://yoosofan.github.io/slide/os.paging.step4pdf.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/os.paging.step4pdf.html>`_

Sample 2
--------
* `rst input source <https://github.com/yoosofan/slide/blob/main/db.sql2.rst>`_
    * `download <http://yoosofan.github.io/slide/db.sql2.rst>`_
* `prezentation output html <https://yoosofan.github.io/slide/db.sql2.presentation.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/db.sql2.presentation.html>`_
* `output of concise html for pdf <https://yoosofan.github.io/slide/db.sql2.concise4pdf.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/db.sql2.concise4pdf.html>`_
* `output of step html for pdf <https://yoosofan.github.io/slide/db.sql2.step4pdf.html>`_
    * `download <https://github.com/yoosofan/slide/blob/main/db.sql2.step4pdf.html>`_

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

    prezento input.rst -o output4presentation.html
    prezento input.rst -s  # Generate input.substep4pdf.html — Step-by-step version
    prezento input.rst -np # Skip b6plus version for screen presentation

Convert to Pdf
--------------
Open `*.concise4pdf.html` output file by any web browser and print it. It would be better if you use landscape and enable background.


Output Targets Pipeline
=======================

A single execution of `prezento` generates up to three distinct structural outputs, tailored for different instructional needs:

1. **Concise Handout Mode (``*.concise4pdf.html``)**
   Outputs a flattened, continuous HTML document. All animation states and incremental steps are fully visible immediately. This is optimized for quick student reference, screen readers, or standard single-pass PDF printing.

2. **Step Handout Mode (``*.step4pdf.html``)**
   Powered by a custom AST deep-cloning engine. If a slide contains progressive steps, the engine clones the slide node entirely for each step, altering the visibility classes sequentially. This produces a long-form HTML file that, when printed to PDF, acts as a perfect flip-book mimicking the exact timing and progression of the live lecture.

3. **Interactive Presentation Mode (``*.presentation.html``)**
   The dynamic projector mode. It automatically maps your logical slide boundaries and step flags into `b6plus` native classes (like ``incremental``) and injects the necessary CSS/JS routing for live speaker delivery.

Syntax and File Structure
=========================

Presentations are written as standard `.rst` files. The document must begin with the ``prezento`` directive to establish global metadata, followed by four-space indented ``slido`` blocks.

.. code:: rst

    .. prezento:: Advanced Memory Management (By Dr. Turing)
       :css: assets/theme.css
       :js: assets/custom_interactions.js

    .. slido:: Introduction to Paging
       :id: slide-paging-intro

       Paging eliminates external fragmentation by dividing physical memory into fixed-sized blocks.

       * Block size is defined by the hardware.
       * Typical sizes range from 4 KB to 8 KB.

    .. slido:: The Translation Look-aside Buffer (TLB)
       :class: custom-slide-bg

       The TLB is a specialized hardware cache for page table entries.

       #. CPU generates a logical address.
       #. The page number is sent to the TLB.
       #. If a **TLB Hit** occurs, the frame is returned immediately.
       #. If a **TLB Miss** occurs, a memory access is required.

Custom Directives Reference
===========================

`prezento` extends docutils with presentation-specific domain hooks:

``slido``
---------
Defines a hard boundary for a new slide. All content belonging to the slide must be indented by exactly four spaces.

* **Options:**
    * ``:id:`` Binds an explicit HTML ID to the slide section.
    * ``:class:`` Applies custom CSS classes to the slide container.
    * ``:step:`` A boolean flag. When present, it instructs the engine to treat child elements (like list items) as progressive incremental steps.

``grafo``
---------
Embeds vector diagrams via Graphviz DOT syntax. The engine captures the output, sanitizes the XML, and embeds it directly as an inline `<svg>`.
* **Features:** It safely catches the ``:scale:`` attribute and translates it into native CSS transforms (``transform: scale(...)``) to prevent Docutils from attempting to use external image libraries. It also automatically rewrites internal ``step`` classes to ``incremental`` to allow diagram elements to appear step-by-step in `b6plus`.

.. code:: rst

    .. grafo::
       :align: center
       :scale: 120

       digraph G {
           node [shape=box];
           "Logical Address" -> "Page Table" [class="step"];
           "Page Table" -> "Physical Memory" [class="step"];
       }

``komento``
-----------
Establishes a private presenter notes block. During the rendering of the ``presentation.html`` target, content inside this directive is wrapped in a ``<section class="comment">``. The `b6plus` engine automatically detects this class, hiding the content from the main projector view while displaying it clearly on the speaker's private control monitor.

.. code:: rst

    .. slido:: Addressing Hardware

       * Page Offset (d)
       * Page Number (p)

       .. komento::

          Make sure to write the formula "m - n" on the whiteboard before switching to the next slide.

Project Structure (Development)
===============================

.. code-block:: text

    prezento/
    ├── src/
    │   └── prezento/
    │       ├── __init__.py
    │       └── main.py     # Core translation pipeline & CLI entry point
    ├── docs/
    │   └── CHANGELOG.rst   # Version history and migration notes
    └── tools/
        ├── readme.rst
        ├── slido_ls.py     # Language Server Protocol (LSP) for IDEs and editors
        ├── build.sh        # Packaging and deployment script
        └── clean.sh        # Environment scrub utility

Contributing
============

Contributions from the educational and open-source communities are highly encouraged. As the project remains in active development, you can assist by:

* Opening detailed issues for rendering bugs or feature requests.
* Submitting Pull Requests to enhance the HTML5 translator logic or add new directive capabilities.
* Testing the pipeline against massive, highly complex academic slide decks to identify edge-case layout breaks.

License
=======

This project is licensed under the **GNU General Public License v3.0** (GPLv3).

See the ``LICENSE`` file in the repository root for the full legal text. You are free to use, modify, and distribute this software strictly under the terms of this license.

Acknowledgments
===============

* Architecture heavily inspired by `Hovercraft <https://github.com/regebro/hovercraft>`_ and the historical framework of `prezentprogramo <https://github.com/yoosofan/prezentprogramo>`_.
* Interactive projector routing powered entirely by the excellent `b6plus <https://www.w3.org/Talks/Tools/b6plus/>`_ framework.
* Structural tree manipulation built on top of the robust Python `docutils <https://docutils.sourceforge.io/>`_ engine.

Author
======

**Ahmad Yoosofan**

- GitHub: https://github.com/yoosofan
- Slides: https://github.com/yoosofan/slide
