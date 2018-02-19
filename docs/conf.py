# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import flask_snow

extensions = ['sphinx.ext.autodoc']
#templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'flask-snow'
copyright = u'2018, Robert Wikman'

version = release = flask_snow.__version__

exclude_patterns = ['_build']

pygments_style = 'sphinx'
html_theme_options = {'github_fork': 'rbw0/flask-snow', 'index_logo': False}

html_theme = 'flask'

#html_static_path = ['_static']

htmlhelp_basename = 'flask-snowdoc'

latex_documents = [
  ('index', 'flask-snow.tex', u'flask-snow Documentation',
   u'Robert Wikman', 'manual'),
]

man_pages = [
    ('index', 'flask-snow', u'flask-snow Documentation',
     [u'Robert Wikman'], 1)
]
