Storage Space
=============

.. code-block::

  sudo apt autoremove -y
  sudo apt clean
  docker image prune -a

  # Note: Carefully select which ones to remove. Some may still be in use
  flatpak uninstall --unused
