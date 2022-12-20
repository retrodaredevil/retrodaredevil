retrodaredevil
=======================================

This contains documentation, resources, and blog posts for Lavender Shannon


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

