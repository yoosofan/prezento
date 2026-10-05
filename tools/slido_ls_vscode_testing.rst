Testing slido_ls.py in VS Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:OS: Windows
:Editor: VS Code
:Python: 3.12.1 (32-bit)
:Language Server: slido_ls.py
:VS Code Extension: Generic LSP Client (v2), zsol.vscode-glspc, v0.2.1

Setup
`````

Installed the Generic LSP Client and reStructuredText extensions.
Configured ``.vscode/settings.json`` to launch ``slido_ls.py`` as the
language server for ``restructuredtext`` files.

Verifying the server
`````````````````````
    
Confirmed the server path and Python installation (``python --version``
→ 3.12.1). Running ``slido_ls.py`` directly in a terminal produced no
errors; the process simply idled, waiting for input on stdin.

Client log observations
```````````````````````

The log first showed ``No server command, not starting glspc``.
After fixing the settings, it showed ``starting glspc: python ...\slido_ls.py``, confirming the extension launches the process.
Occasional ``couldn't create connection to server`` / ``Server‌‌ process exited`` errors were resolved by the same settings fix.

Tested standard RST files
`````````````````````````

For plain reStructuredText files, ``Ctrl+Shift+O`` correctly listed
section headers, though the extension's Output panel stayed empty.

Tested Prezento files
`````````````````````

For files using ``.. prezento::`` and ``.. slido::``, ``Ctrl+Shift+O``
reported "No editor symbols", and the Output panel was empty.
VS Code's status bar still correctly showed the file type as
reStructuredText.

Conclusion
``````````

Python, the file path, and the server itself all work correctly, and
the extension does launch the process. The problem is isolated to
Prezento symbols specifically: the LSP messages needed to extract
them are not being exchanged correctly, or the extension cannot use
the server's responses.