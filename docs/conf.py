# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0,os.path.abspath('../'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","GestorDeProyectosAgiles.settings.desarrollo")

project = 'GestorDeProyectosAgiles'
copyright = '2022, Aramy Rolon, Alisha Rotela, Araceli Valenzuela, Jennifer Staple'
author = 'Aramy Rolon, Alisha Rotela, Araceli Valenzuela, Jennifer Staple'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc','sphinx.ext.ifconfig','sphinx_rtd_theme']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
