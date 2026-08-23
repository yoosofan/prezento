Styling presentations
=====================

Include your own CSS
--------------------

Pass stylesheets in the ``prezento`` directive:

.. code-block:: rst

   .. prezento:: Course title
      :css: ./assets/style.css

Several files, comma-separated:

.. code-block:: rst

   :css: ./assets/style.css, ./assets/rtl.css

In presentation HTML, user CSS is linked **before** prezento's small
b6plus helper stylesheet so you can override defaults.

Adding JavaScript
-----------------

.. code-block:: rst

   :js: ./assets/custom.js

Unlike Hovercraft there is no ``:js-header:`` / ``:js-body:`` split and
no ``--js`` CLI flag. Keep scripts next to the deck; ``--outdir`` will
copy local ones.

Per-slide classes
-----------------

.. code-block:: rst

   .. slido:: Two column example
      :class: t2c
      :id: unique-slide-id

Then in CSS::

    section#unique-slide-id {
        background: #f7f4ee;
    }

    section.t2c {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
    }

Prefer **ids** for one-off styling. Sequence-based ids would break when
you insert a slide; ``:id:`` stays stable.

Layout helpers used in the sample decks
---------------------------------------

These are **not** built into prezento; they live in your
``assets/style.css`` (see the slide repository). Common conventions:

========== ==========================================================
Class      Typical use
========== ==========================================================
``t2c``    Two-column slide
``t3c``    Three-column slide
``n2c``    Narrow / numeric two-column
``rtl``    Right-to-left (also ``ltr``)
``rtl-h1`` Persian/Arabic heading (also ``rtl-h2``)
========== ==========================================================

Images
------

.. code-block:: rst

   .. image:: figures/tlb.png
      :align: center
      :scale: 90%
      :height: 550px
      :class: step

Pillow must be installed (it is a prezento dependency) or docutils
cannot honour ``:scale:``.

Graphviz sizing
---------------

Graphviz writes ``width``/``height`` in points on the ``<svg>``.
prezento strips those attributes when you pass ``:width:`` or
``:height:`` on ``grafo``, then injects your values so CSS can scale
the diagram.

Custom fonts
------------

For conference machines without network access, **bundle fonts** in
``assets/fonts/`` and ``@font-face`` them in your CSS. Do not rely on
Google Fonts URLs in an air-gapped hall.

Hovercraft copies ``@font-face`` files automatically when you pass a
target directory. prezento’s equivalent is ``-d`` / ``--outdir``, which
copies local resources it can discover from the RST/HTML.

The same rule applies to MathJax: if you need math rendering beyond
plain CSS, ship a local copy and load it with ``:js:``.

Print
-----

Concise/step HTML is meant to be printed from the browser. A print
stylesheet can hide ``.slide-number`` or tighten padding::

    @media print {
        section.slide {
            break-after: page;
        }
    }

Presentation HTML already sets ``break-after: auto`` and hides
``.slide-number`` while ``body.full``.

b6plus visual hooks
-------------------

While projecting, b6plus sets:

* ``body.full`` — slide mode
* ``.active`` / ``.visited`` on slides and incrementals
* ``--progress`` CSS variables if you add a progress element

Style incrementals so hidden items do not leave a large empty hole, or
accept the default ``visibility: hidden`` from prezento's helper CSS.

Design advice
-------------

* Keep type large enough for the back row (never below ~22px on the
  projector stylesheet).
* Prefer one diagram per slide; use steps instead of crowding.
* Test both the concise printout and the live deck — they share
  content but not layout constraints.
* Mixed RTL/LTR lectures: wrap phrases in roles (``:rtl:`` / ``:ltr:``)
  defined at the top of the RST file.
* b6plus is linear. There is no impress.js zoom; do not try to fake
  3-D with CSS transforms on ``section.slide`` — it fights slide mode.
