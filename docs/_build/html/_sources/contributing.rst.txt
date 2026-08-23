Contributing
============

Contributions from the educational and open-source communities are welcome.
The project is in active use for university lectures; the most useful
help is:

* Opening detailed issues for rendering bugs or feature requests.
* Pull requests that improve the HTML5 translator or add directives.
* Testing against large academic decks (mixed RTL/LTR, heavy ``grafo``,
  many steps).

Repository
----------

https://github.com/yoosofan/prezento

Project layout
--------------

.. code-block:: text

   prezento/
   ├── src/prezento/
   │   ├── __init__.py
   │   └── main.py          # Directives, writers, CLI
   ├── docs/                # This Sphinx / Read the Docs tree
   │   ├── conf.py
   │   ├── index.rst
   │   └── CHANGELOG.rst
   ├── tools/
   │   ├── slido_ls.py      # LSP for slide outlines
   │   ├── build.sh
   │   ├── clean.sh
   │   └── readme.rst
   ├── pyproject.toml
   ├── README.rst
   └── LICENSE.txt

Where to patch
--------------

Almost all compiler behaviour lives in ``src/prezento/main.py``:

* Directive and node classes at the top (``prezento``, ``slido``,
  ``grafo``, ``komento``)
* Step expansion (``_expand_slide``, ``_assign_reveal_indices``)
* b6plus transform (``_b6_transform`` — ``step`` → ``incremental``)
* HTML translators (``SlidoTranslator``, ``PresentationSlidoTranslator``)
* Standalone folder (``build_standalone_folder``)
* CLI ``main()``

``tools/slido_ls.py`` is a separate stdlib-only LSP (no prezento import).

Development install
-------------------

.. code-block:: bash

   git clone https://github.com/yoosofan/prezento.git
   cd prezento
   pip install -e .
   prezento --help

Building this documentation
---------------------------

.. code-block:: bash

   pip install -r docs/requirements.txt
   cd docs
   make html

Output is ``docs/_build/html/index.html``. Read the Docs uses
``.readthedocs.yaml`` at the repository root.

License
-------

GNU GPL v3.0 or later. See ``LICENSE.txt``.
