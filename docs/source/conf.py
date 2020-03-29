import sys
import os
import shlex

sys.path.insert(0, os.path.abspath("."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "IPython.sphinxext.ipython_console_highlighting",
]

templates_path = ["_templates"]

autodoc_member_order = "bysource"

source_suffix = ".rst"

master_doc = "index"

project = u"lasio"
copyright = u"2013-2020, Kent Inverarity and contributors"
author = u"Kent Inverarity and contributors"

version = "0.25"
release = "0.25.0"

language = None

exclude_patterns = []

pygments_style = "default"

todo_include_todos = True

html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}
html_theme_options = {}


htmlhelp_basename = "lasiodoc"

latex_elements = {}

latex_documents = [
    (
        master_doc,
        "lasio.tex",
        u"lasio Documentation",
        u"Kent Inverarity and contributors",
        "manual",
    )
]

man_pages = [(master_doc, "lasio", u"lasio Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "lasio",
        u"lasio Documentation",
        author,
        "lasio",
        "One line description of project.",
        "Miscellaneous",
    )
]

intersphinx_mapping = {"https://docs.python.org/": None}
