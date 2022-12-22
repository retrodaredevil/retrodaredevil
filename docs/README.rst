retrodaredevil
=======================================

This contains documentation, resources, and blog posts for Lavender Shannon

Cheat sheet for Restructured Text format: https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html


Building
----------

To build this yourself, run these commands:

.. code-block:: shell

  cd docs/
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r source/requirements.txt
  make html
  xdg-open "file://$(pwd)/build/html/index.html"
  make latexpdf  # requires latexmk command
  make epub


Editing
--------

I recommend using VS Code to edit. Press CTRL+P and paste the below to setup recommended extensions:

.. code-block::

  ext install EditorConfig.EditorConfig
  ext install trond-snekvik.simple-rst
  ext install lextudio.restructuredtext

``EditorConfig.EditorConfig`` is for EditorConfig support, ``trond-snekvik.simple-rst`` is for syntax highlighting.
``lextudio.restructuredtext`` is for live preview.

Once you install ``lextudio.restructuredtext``, you will be asked to install the language server after enabling. 
Say yes. In the top right, there is an "Open preview" button.

In VS Code, opening links will result in a new browser window: https://stackoverflow.com/a/64700513/5434860.
To resolve, navigate to ``about:profiles`` in the new window and make the "default-release" profile the default profile.
