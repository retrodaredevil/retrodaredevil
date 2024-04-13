July 2023 Nasplex to Proxmox
================================

Today on July 14, 2023 me and Dave are backing up Nasplex, which is currently running OMV.

Backing up
--------------

I ran this:

.. code-block:: shell

  sudo rsync -a --partial --progress containers /srv/dev-disk-by-uuid-283fd7ec-f405-431d-b763-1ff321fa60d3/

.. code-block:: console

  lavender@nasplex:~$ id
  uid=1001(lavender) gid=100(users) groups=100(users),0(root),5(tty),20(dialout),27(sudo),33(www-data),37(operator),44(video),113(ssh),995(openmediavault-notify),996(openmediavault-webgui),997(openmediavault-admin),998(openmediavault-engined),999(openmediavault-config),1000(solarthing)
  lavender@nasplex:~$ id solarthing
  uid=996(solarthing) gid=1000(solarthing) groups=1000(solarthing),5(tty),20(dialout),44(video)
  lavender@nasplex:~$ cat .gitconfig
  [user]
          name = Lavender Shannon
          email = retrodaredevil@gmail.com
          signingkey = 2C0C6D38777562E5
  [commit]
          gpgsign = true
  [tag]
          gpgsign = true

``/etc/fstab`` is this:

.. code-block::

  # /etc/fstab: static file system information.
  #
  # Use 'blkid' to print the universally unique identifier for a
  # device; this may be used with UUID= as a more robust way to name devices
  # that works even if disks are added and removed. See fstab(5).
  #
  # systemd generates mount units based on this file, see systemd.mount(5).
  # Please run 'systemctl daemon-reload' after making changes here.
  #
  # <file system> <mount point>   <type>  <options>       <dump>  <pass>
  # / was on /dev/sda2 during installation
  UUID=2c2ed961-8a91-41c0-a24e-c0f66eb18ea7 /               ext4    errors=remount-ro 0       1
  # /boot/efi was on /dev/sda1 during installation
  UUID=156A-34A0  /boot/efi       vfat    umask=0077      0       1
  # swap was on /dev/sda3 during installation
  UUID=d6ca006f-5162-4fbe-b85c-4e3c7d97564f none            swap    sw              0       0
  # >>> [openmediavault]
  /dev/disk/by-uuid/283fd7ec-f405-431d-b763-1ff321fa60d3          /srv/dev-disk-by-uuid-283fd7ec-f405-431d-b763-1ff321fa60d3      ext4    defaults,nofail,user_xattr,usrjquota=aquota.user,grpjquota=aquota.group,jqfmt=vfsv0,acl  0 2
  /dev/disk/by-uuid/9ee13bdb-0212-4dd1-b552-a4453010e947          /srv/dev-disk-by-uuid-9ee13bdb-0212-4dd1-b552-a4453010e947      ext4    defaults,nofail,user_xattr,usrjquota=aquota.user,grpjquota=aquota.group,jqfmt=vfsv0,acl  0 2
  # <<< [openmediavault]

Setting up Proxmox
--------------------

We created a ``lavender`` user for myself, but to give it access to the web ui we had to run:

.. code-block:: shell

  sudo pveum user add lavender@pam

That let me login to the web interface, but I had no permissions.
``sudo pveum group list`` indicates that there are no groups created yet.
All I have to do is follow the Administrator example on this page: https://pve.proxmox.com/wiki/User_Management

.. code-block:: shell

  sudo pveum group add admin -comment "System Administrators"
  sudo pveum acl modify / -group admin -role Administrator
  sudo pveum user modify lavender@pam -group admin

Mounting the External Drive
-----------------------------

We mounted the external drive just like last time I did this on my install.
But, we wanted to add 100000 to each file in the drive so that containers could access everything on the drive.

I asked ChatGPT "Let's say I have a directory with some files and folders in it. Pretty standard. I want to take each owner and group id and add 100000 to it. Give me a command to do that"
It told me this:

.. code-block:: shell

  sudo find /srv/dev-disk-by-uuid-283fd7ec-f405-431d-b763-1ff321fa60d3/ -exec sh -c 'chown $(($(stat -c "%u" "{}")+100000)) "{}" && chgrp $(($(stat -c "%g" "{}")+100000)) "{}"' \;

The command took forever to execute, but it eventually finished. (The command took like an hour).

Wireguard setup
----------------

I installed PiVPN using https://tteck.github.io/Proxmox/.
After some research I realized that PiVPN isn't going to be able to handle working as a client,
at least not without doing plain wireguard configuration.
I'm going to come back to this at some point, but I likely won't use PiVPN here. I will probably create my own Linux container.
