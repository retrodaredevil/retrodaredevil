# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Lavender Docs'
copyright = '2022, Lavender Shannon'
author = 'Lavender Shannon'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx_reredirects', # https://documatt.gitlab.io/sphinx-reredirects/install.html
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Based on https://github.com/wildmountainfarms/solarthing-docs/blob/78341f6a55b910e4036d15107e582920bcb104a4/docs/source/conf.py#L40
extlinks = {
    'docker-hub': ('https://hub.docker.com/r/%s', '%s'),
}

# https://documatt.gitlab.io/sphinx-reredirects/usage.html
redirects = {
    "blog/2023-05-building-new-server-running-linux": "blog/tech/2023-05-building-new-server-running-linux.html"
}
