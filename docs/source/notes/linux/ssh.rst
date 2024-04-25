SSH
=====

SSH is awesome! It's useful for so many things! This page aims to document some of them, and how I use them.

Authorizing Users
--------------------

To authorize someone to log in to your machine, one would typically use the ``$HOME/.ssh/authorized_keys`` file.
You can find out more about this file here: https://www.ibm.com/docs/en/zos/2.4.0?topic=daemon-format-authorized-keys-file

SSH Tunnels
------------

There are many ways to use tunnels. This blog post describes it very well: https://iximiuz.com/en/posts/ssh-tunnels/.


Mosh
-----

Mosh is a great application to use with SSH to make your SSH sessions more stable.

UTF-8 locale needed
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

  The locale requested by LANG=en_US.UTF-8 isn't available here.
  Running `locale-gen en_US.UTF-8' may be necessary.

  mosh-server needs a UTF-8 native locale to run.

  Unfortunately, the local environment (LANG=C) specifies
  the character set "US-ASCII",

  The client-supplied environment (LANG=en_US.UTF-8) specifies
  the character set "US-ASCII".

If you get this error, you likely need to run this on the server you are trying to access:

.. code-block::

  sudo apt update && sudo apt install locales
  sudo locale-gen en_US.UTF-8
  # If that doesn't work, then run this:
  # When running this, just choose "en_US.UTF-8"
  sudo dpkg-reconfigure locales

See my answer here: https://unix.stackexchange.com/a/765013/591317
