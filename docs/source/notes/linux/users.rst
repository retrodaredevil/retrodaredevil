Users
======

Managing users is a reoccurring task that I do often.

User Creation
---------------

.. code-block:: shell

  # Note that the most important group here is sudo
  useradd --create-home --user-group --shell /usr/bin/bash --groups sudo,tty,dialout,video,docker,input lavender
  passwd lavender
  mkdir /home/lavender/.ssh
  vi /home/lavender/.ssh/authorized_keys
  chown -R lavender:lavender /home/lavender/.ssh && chmod 700 /home/lavender/.ssh && chmod 600 /home/lavender/.ssh/authorized_keys

.. note::

  Remember to make sure sudo is installed ``apt update && apt install -y sudo``

  As another friendly reminder, you probably don't have ``vim`` installed, and may benefit by looking at

Proxmox Authorization
----------------------

Add a user to Proxmox:

.. code-block:: shell

  sudo pveum user add lavender@pam

Create the admin group and give your user permissions:

.. code-block:: shell

  sudo pveum group add admin -comment "System Administrators"
  sudo pveum acl modify / -group admin -role Administrator

  sudo pveum user modify lavender@pam -group admin

SSH Key Creation
----------------

.. code-block:: shell

  ssh-keygen -t ed25519
  cat ~/.ssh/id_ed25519.pub

https://github.com/settings/keys

.. note::

  If authentication with Azure DevOps is a requirement, use the ``rsa-sha2-512`` key type.
