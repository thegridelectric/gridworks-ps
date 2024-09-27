"""Sphinx configuration."""

project = "GridWorks Price Service"
author = "gridworks"
copyright = "2023, gridworks"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
