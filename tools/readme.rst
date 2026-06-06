=============================
Prezento Developer Utilities
=============================

This directory contains complementary tools designed to enhance productivity when developing or working with `prezento`. To keep the core package lightweight and minimize external dependencies, these optional scripts are maintained separately here rather than being bundled into the main distribution.

.. contents:: Table of Contents
   :depth: 4

Scripts and Files
=================

slido_ls.py
-----------

This script acts as a specialized Language Server Protocol (LSP) server that integrates slide numbers into compatible text editors and IDEs. It parses `prezento` reStructuredText slide source files, tracks individual slides, and provides context descriptions. This allows slide authors and readers to seamlessly map the source structure to the generated HTML output.

It does not interfere with standard reStructuredText files; it explicitly scans for the `.. prezento::` directive. If the directive is absent, it treats the file normally while still providing enhanced symbol tree functionality to your editor.

.. note::
   This server was initially scaffolded and refined via extensive automated prototyping and targeted constraint testing to ensure robust edge-case handling.

Deployment and Editor Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Make the script executable on Unix-based systems:

   .. code:: sh

       chmod a+x slido_ls.py

2. Configure your editor or IDE to invoke this script as an LSP server for the ``rst`` file type. Below are setup examples for popular editors.

.. important::
   In the configuration examples below, the path ``/home/absolute/path/to/here/prezento/tools/slido_ls.py`` is a placeholder. You must replace it with the actual, absolute absolute path to where the ``slido_ls.py`` file is located on your local machine.

Kate Editor
````````````````

1. Navigate to **Settings** > **Configure Kate**.
2. In the configuration window, select **Plugins** from the left-hand navigation sidebar.
3. Check the box next to **LSP Client** to enable the plugin, then click **Apply**.
4. Switch to the newly visible **LSP Client** settings tab.
5. Select the **User Server Settings** sub-tab and insert the following JSON configuration (adjusting the absolute path to point to your local repository clone):

   .. code:: json

       {
           "servers": {
               "rst": {
                   "command": ["/home/absolute/path/to/here/prezento/tools/slido_ls.py"],
                   "rootIndicationFileNames": [],
                   "highlightingModeRegex": "^reStructuredText$"
               }
           }
       }

Neovim (Built-in LSP client)
```````````````````````````````````

If you are using Neovim's built-in LSP client, you can spawn the server manually whenever an ``rst`` file type is loaded. Add the following snippet to your ``init.lua`` file or your ``ftplugin/rst.lua`` file:

.. code:: lua

    vim.api.nvim_create_autocmd("FileType", {
        pattern = "rst",
        callback = function()
            vim.lsp.start({
                name = "slido-ls",
                cmd = { "/home/absolute/path/to/here/prezento/tools/slido_ls.py" },
                root_dir = vim.fs.root(0, { ".git", "pyproject.toml" }),
            })
        end,
    })

The primary scope of this tool is focused on generating a clean, accurate symbol tree navigation pane for individual slide elements during active editing sessions.

Visual Studio Code (via LSP Config)
```````````````````````````````````

VS Code typically requires compiling a standalone extension framework to execute custom binaries. You can bypass this by running your local server through the third-party `LSP Config <https://marketplace.visualstudio.com/items?itemName=pepebecker.vscode-lsp-config>`_ extension.

Once installed, append this server block profile to your global ``settings.json`` file:

.. code:: json

    {
        "lsp-config.servers": {
            "prezento-slido": {
                "command": ["/home/absolute/path/to/here/prezento/tools/slido_ls.py"],
                "filetypes": ["restructuredtext"]
            }
        }
    }


Development Background & Acknowledgments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool is the result of an intensive, iterative co-development process between the project author and Gemini AI. Bringing this script to its current state required hours of rigorous prompting, constraint testing, and systematic code adjustments. This collaborative effort ensured that the server satisfies strict functional requirements and safely navigates edge cases without introducing processing regressions.

clean.sh
--------

A utility script designed to purge transient build files and automatically generated workspace clutter. Maintaining a minimal workspace footprint ensures project clarity and prevents build artifacts from interfering with development environments.

build.sh
--------

A localized build verification script used to test code changes safely. Rather than executing tests directly within the core repository directories, it clones workspace states to isolated pathways for testing. The latter portion of this file contains code comments detailing routine maintenance and testing instructions.

Shell Customization Utilities
=============================

Optimized Tab-Completion Alias (``prz``)
----------------------------------------

To substitute the standard ``prezento`` command with a faster ``prz`` shorthand—while simultaneously restricting shell tab-completion strictly to ``.rst`` files—append the following lines to your local ``~/.bashrc`` file:

.. code-block:: sh

    # 1. Create your abbreviated shortcut
    alias prz="prezento"

    # 2. Enforce .rst filtering AND allow directory navigation
    complete -f -X '!*.rst' -o default prz

This configuration leverages native Linux Bash built-ins, eliminating the need for third-party completion frameworks or root-level modifications inside system directories like ``/etc/bash_completion.d/``.
