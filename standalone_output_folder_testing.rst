Testing the Standalone Output Folder Feature (-d)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tested on Windows with Python 3.12.1, prezento installed via
``pip install -e .``.

Folder creation
```````````````

Running ``prezento input.rst -d output_folder`` creates a folder
containing ``index.html`` (same as presentation), the concise4pdf
HTML, and an auto-generated ``list_of_resources.rst`` manifest.
The default presentation and concise4pdf files are still written
next to the source file as well; ``-d`` adds a standalone copy
rather than replacing the default output.

Resource copying
`````````````````

Image, CSS, and JS library files were copied correctly into the
folder (``3 copied, 0 missing, 0 external``), and all paths in the
generated HTML are relative rather than absolute.

Interaction bug: -s combined with -d
`````````````````````````````````````

When ``-s`` and ``-d`` are used together, ``step4pdf`` is generated
correctly next to the source file but is **not** copied into the
standalone folder, while presentation and concise4pdf are. Each
flag works correctly on its own.

Portability
```````````

Moving the whole output folder to a different path, zipping and
re-extracting it elsewhere, and opening it with no internet
connection all worked correctly — images, styling, and slide
navigation remained intact. Moving a single HTML file without its
resource folder correctly failed to render, confirming the relative
paths work as intended.

file:// vs local server
```````````````````````

Opening the output by double-clicking (``file://`` protocol)
triggers a browser security error when navigating between slides
("Unsafe attempt to load URL ... unique security origins").
Serving the same folder through a local HTTP server
(``python -m http.server``) resolves this completely, with no
console errors.

Summary
````````

The standalone folder feature works well for resource copying and
portability. Two issues were found: ``step4pdf`` is missing from
the standalone folder when combined with ``-s``, and direct
``file://`` access causes a navigation error that a local server
avoids.