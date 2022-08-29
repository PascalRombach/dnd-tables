import sys, os
sys.path.append(os.path.abspath("./_ext"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'D&D Tabellen'
copyright = '2022, Fisch37'
author = 'Fisch37'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "rollingtables",
    "sphinx.ext.autosectionlabel"
]

templates_path = ['_templates']
exclude_patterns = []

language = 'de'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_js_files = [
    "tables.js"
]
html_css_files = [
    "tables.css"
]