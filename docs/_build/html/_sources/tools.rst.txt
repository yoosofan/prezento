Editor tools
============

Language server (``slido_ls.py``)
---------------------------------

``tools/slido_ls.py`` is a small **Language Server Protocol** server
aimed at reStructuredText files. It is not a full Sphinx/Esbonio
replacement: it exists so editors can show a **symbol outline** of
slides.

The script is **stdlib-only** (``sys``, ``json``, ``re``) and is not
installed by ``pip install prezento``. Clone the repository or copy the
file.

Behaviour
~~~~~~~~~

* If the buffer contains ``.. prezento::``, the server is in
  **presentation mode**. Each ``.. slido::`` becomes a top-level symbol
  named ``(n) Title`` (or ``(n) [Untitled Slide]``).
* Otherwise it outlines ordinary RST **section titles** as a tree.

Implemented LSP methods:

* ``initialize`` (full text sync, ``documentSymbolProvider``)
* ``textDocument/didOpen``
* ``textDocument/didChange``
* ``textDocument/documentSymbol``

Why not Esbonio?
~~~~~~~~~~~~~~~~

`Esbonio <https://github.com/swyddfa/esbonio>`_ is an excellent LSP
for **Sphinx projects**. Standalone lecture files (no ``conf.py``,
custom ``slido`` / ``grafo`` / ``komento``) often fail to initialise
it. ``slido_ls.py`` only needs the RST text.

Kate
~~~~

1. Make the script executable::

       chmod a+x tools/slido_ls.py

2. Settings → Configure Kate → Plugins → enable **LSP Client**.
3. LSP Client → **User Server Settings**::

       {
           "servers": {
               "rst": {
                   "command": ["/absolute/path/to/prezento/tools/slido_ls.py"],
                   "rootIndicationFileNames": [],
                   "highlightingModeRegex": "^reStructuredText$"
               }
           }
       }

Neovim
~~~~~~

In ``init.lua`` or ``ftplugin/rst.lua``::

    vim.api.nvim_create_autocmd("FileType", {
        pattern = "rst",
        callback = function()
            vim.lsp.start({
                name = "slido-ls",
                cmd = { "/absolute/path/to/prezento/tools/slido_ls.py" },
                root_dir = vim.fs.root(0, { ".git", "pyproject.toml" }),
            })
        end,
    })

Geany
~~~~~

Geany’s built-in ctags sidebar does not understand ``slido``. Use the
`geany-lsp <https://github.com/techee/geany-lsp/>`_ plugin.

1. Tools → Plugin Manager → enable **LSP Client**.
2. Tools → LSP Client → **User Configuration**.
3. Append::

       [restructuredtext]
       cmd=/absolute/path/to/prezento/tools/slido_ls.py

4. Tools → LSP Client → **Restart All Servers**.

The **Symbols** sidebar then lists numbered slides.

A dedicated ctags-style ``*.rst.tags`` generator was removed in v1.0.3
in favour of this server.

Visual Studio Code
~~~~~~~~~~~~~~~~~~

VS Code has no built-in way to run an arbitrary LSP binary. One option
is the `LSP Config <https://marketplace.visualstudio.com/items?itemName=pepebecker.vscode-lsp-config>`_
extension::

    {
        "lsp-config.servers": {
            "prezento-slido": {
                "command": ["/absolute/path/to/prezento/tools/slido_ls.py"],
                "filetypes": ["restructuredtext"]
            }
        }
    }

Helper scripts
--------------

``tools/build.sh``
    Packaging / deployment helper for maintainers.

``tools/clean.sh``
    Environment scrub.

``tools/readme.rst``
    Longer notes for the tools directory, including a ``prz`` bash
    alias that tab-completes only ``*.rst`` files::

        alias prz="prezento"
        complete -f -X '!*.rst' -o default prz
