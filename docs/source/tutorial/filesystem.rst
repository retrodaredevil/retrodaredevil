Filesystem
==========

This page aims to document getting around a Linux file system

Automatically mounting with ``/etc/fstab``
--------------------------------------------

If you have a hard drive that you want mounted, you can edit your ``/etc/fstab`` file.
First, you will want to get the UUID of your device. Note this UUID will appear to be a different format or length depending on the format of your drive.

You can use ``ls -l /dev/disk/by-uuid/`` to list a bunch of UUIDs, although it may be hard to determine which one is your drive.
You can also use ``lsblk``, which can be installed via ``sudo apt install libblkid1``. Now run ``lsblk -f``.

Once you have the UUID of your device, you can edit ``/etc/fstab`` and add lines such as:

.. code-block::

  UUID=2b941c0d-aee9-3377-88ff-fcad0224ede9 /srv/lavender_drive1 ext4 defaults,nofail 1 1

Editing the ``/etc/fstab`` file will not have any affect until the system is restarted. 
I actually recommend getting your settings and mountpoint setup using the ``mount`` command, which is not talked about on this page.
