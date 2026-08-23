Installation
============

Requirements
------------

* Python **3.10** or newer
* `docutils <https://docutils.sourceforge.io/>`_ ≥ 0.21
* Pygments ≥ 2.20 (syntax highlighting)
* graphviz Python package ≥ 0.20 **and** the Graphviz binaries on ``PATH``
  (only needed if you use the ``grafo`` directive)
* Pillow ≥ 12.1 (image ``:scale:``, ``:width:``, ``:height:``)

Install from PyPI
-----------------

.. code-block:: bash

   pip install prezento

The console script ``prezento`` is installed as
``prezento.main:main``.

Install from source
-------------------

Recommended while developing or tracking ``main``:

.. code-block:: bash

   git clone https://github.com/yoosofan/prezento.git
   cd prezento
   pip install -e .

The package uses a ``src/`` layout defined in ``pyproject.toml``.

Graphviz system package
-----------------------

The ``grafo`` shells out to the Graphviz ``dot`` program. On Debian/Ubuntu:

.. code-block:: bash

   sudo apt install graphviz

On Fedora:

.. code-block:: bash

   sudo dnf install graphviz

On macOS (Homebrew):

.. code-block:: bash

   brew install graphviz

Without the binary, ``grafo`` still parses, but the SVG will be empty.

b6plus runtime asset
--------------------

Generated **presentation** HTML loads:

.. code-block:: text

   assets/b6plus.js

After generating files, place an ``assets/`` directory **next to** the HTML
output containing ``b6plus.js``.

Obtain it from:

* https://www.w3.org/Talks/Tools/b6plus/slides.zip
* https://github.com/yoosofan/slide/tree/main/assets

The ``-d`` / ``--outdir`` flag copies referenced local resources (including
``b6plus.js`` if it is found) into a self-contained folder.

Verify the install
------------------

.. code-block:: bash

   prezento --help
   prezento path/to/sample.rst
