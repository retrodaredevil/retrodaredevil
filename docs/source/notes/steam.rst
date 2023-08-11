Steam on Linux
================

.. note:: 

  This is work in progress and is intended to be a guide for my future self.

Steam is fairly straigt forward to download and install.
You can download it here: https://store.steampowered.com/about/download.
This guide will focus on installation on a remote Linux machine.

Install and Run Steam
-------------------------------

.. note::

  This assumes that you are either physically on the machine where a desktop environment is installed,
  or your SSH session supports X11 forwarding.

.. code-block:: shell

  sudo apt install -y gdebi

  cd ~/Downloads/
  wget https://cdn.akamai.steamstatic.com/client/installer/steam.deb
  sudo gdebi steam.deb

  steam

If everything worked correctly, steam should open up.
Steam may request that certain things be installed.
Even when authenticating, it would error out. I had to manually install the dependencies that steam wanted.

.. code-block:: shell

  # Install whatever dependencies steam wants
  sudo apt install steam-libs-amd64:amd64 steam-libs-i386:i386

Now you can open steam with the ``steam`` command and download a game.
Try streaming the downloaded game from another computer.

