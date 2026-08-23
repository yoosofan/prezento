Examples
========

Companion repository
--------------------

Classroom decks live in https://github.com/yoosofan/slide

Each topic is a single RST file at the repository root:

``<course>.<topic>.rst``

Sample 1 — Operating Systems: Paging
------------------------------------

* `Paging source <https://github.com/yoosofan/slide/blob/main/os.paging.rst>`_
* `Paging presentation <https://yoosofan.github.io/slide/os.paging.presentation.html>`_
* `Paging concise HTML <https://yoosofan.github.io/slide/os.paging.concise4pdf.html>`_
* `Paging step HTML <https://yoosofan.github.io/slide/os.paging.step4pdf.html>`_

This deck shows images with ``:scale:``, mixed English/Persian roles,
``csv-table`` memory maps, ``grafo`` address-translation diagrams,
``komento`` speaker asides, and ``step`` lists for EAT calculations.

Sample 2 — Databases: SQL (part 2)
----------------------------------

* `SQL source <https://github.com/yoosofan/slide/blob/main/db.sql2.rst>`_
* `SQL presentation <https://yoosofan.github.io/slide/db.sql2.presentation.html>`_
* `SQL concise HTML <https://yoosofan.github.io/slide/db.sql2.concise4pdf.html>`_
* `SQL step HTML <https://yoosofan.github.io/slide/db.sql2.step4pdf.html>`_

Minimal skeleton
----------------

A copy of this file is in ``docs/examples/minimal.rst``.

.. literalinclude:: examples/minimal.rst
   :language: rst

Build it::

    prezento demo.rst -s

Then copy ``assets/b6plus.js`` next to the HTML (or use ``-d dist``).

Migrating from Hovercraft / prezentprogramo
-------------------------------------------

1. Replace ``----`` separators with ``.. slido:: Title``.
2. Move document fields such as ``:css:`` into ``.. prezento::``.
3. Replace ``.. note::`` speaker notes with ``.. komento::``.
4. Replace impress.js ``:data-x:`` positioning — b6plus is linear.
5. Rename ``yographviz`` → ``grafo``.
6. Prefer class ``step`` over ``substep``.
7. Re-test print output; that is the main reason to migrate.
