Building this documentation
===========================

This directory is a **Sphinx** project intended for
`Read the Docs <https://readthedocs.io>`_, following the same layout as
`Hovercraft! <https://hovercraft.readthedocs.io>`_ (``conf.py``,
``index.rst``, a ``toctree`` of topic files, ``Makefile``).

Drop this ``docs/`` tree (plus the repository-root
``.readthedocs.yaml``) into https://github.com/yoosofan/prezento and
import the project on Read the Docs.

Local HTML
----------

.. code-block:: bash

   pip install -r docs/requirements.txt
   cd docs
   make html

Open ``docs/_build/html/index.html``.

Read the Docs
-------------

The repository root contains ``.readthedocs.yaml``. Import
https://github.com/yoosofan/prezento on Read the Docs; it will run
Sphinx with ``docs/conf.py`` and the ``sphinx_rtd_theme``.

Page map
--------

* ``index.rst`` — Landing page and toctrees
* ``introduction.rst`` — Why RST, why b6plus, related projects
* ``installation.rst`` — pip, Graphviz, ``b6plus.js``
* ``usage.rst`` — CLI, PDF, Python API
* ``presentations.rst`` — Authoring slides (Hovercraft analogue)
* ``directives.rst`` — ``prezento``, ``slido``, ``grafo``, ``komento``
* ``outputs.rst`` — Concise / step / presentation / ``--outdir``
* ``styling.rst`` — CSS, fonts, print (Hovercraft *designing*)
* ``tools.rst`` — ``slido_ls.py`` for Kate, Neovim, Geany, VS Code
* ``examples.rst`` — Sample decks and a skeleton
* ``faq.rst`` — Common pitfalls
* ``contributing.rst`` — Layout of the compiler
* ``CHANGELOG.rst`` — Version history (GitHub canonical name)
