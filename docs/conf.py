# -*- coding: utf-8 -*-
#
# prezento documentation build configuration file.
# Sphinx / Read the Docs layout, modelled on Hovercraft!'s docs/
# (https://github.com/regebro/hovercraft/tree/master/docs).
#
# This file is execfile()d with the current directory set to its containing dir.

# -- General configuration -----------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "prezento"
copyright = "2026, Ahmad Yoosofan"
author = "Ahmad Yoosofan"

version = "1.1"
release = "1.1.1"

language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "examples", "CHANGELOG.rst", "README.rst"]
pygments_style = "sphinx"
todo_include_todos = False

extlinks = {
    "issue": ("https://github.com/yoosofan/prezento/issues/%s", "#%s"),
    "source": ("https://github.com/yoosofan/prezento/blob/main/%s", "%s"),
}

# -- Options for HTML output ---------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 3,
    "includehidden": True,
    "titles_only": False,
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
}

html_title = "prezento documentation"
html_short_title = "prezento"
html_favicon = "_static/favicon.svg"
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
html_static_path = ["_static"]
html_css_files = ["custom.css"]
htmlhelp_basename = "prezentodoc"

html_context = {
    "display_github": True,
    "github_user": "yoosofan",
    "github_repo": "prezento",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
}

latex_documents = [
    (
        "index",
        "prezento.tex",
        "prezento Documentation",
        "Ahmad Yoosofan",
        "manual",
    ),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    ("index", "prezento", "prezento Documentation", ["Ahmad Yoosofan"], 1)
]

# -- Options for Texinfo output ------------------------------------------------

texinfo_documents = [
    (
        "index",
        "prezento",
        "prezento Documentation",
        "Ahmad Yoosofan",
        "prezento",
        "Modern RST slide generator using b6plus.",
        "Miscellaneous",
    ),
]

# -- Intersphinx ---------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
