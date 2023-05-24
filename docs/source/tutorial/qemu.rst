Qemu
========

For reference: https://christitus.com/vm-setup-in-linux/

Server setup
-----------------

First make sure that virtualization is enabled: :doc:`virtualization`.

.. code-block:: shell

  # On your server
  sudo apt-get install -y qemu-kvm qemu-system qemu-utils libvirt-clients bridge-utils virtinst libvirt-daemon
  # I know for a fact that libvirt-clients, is required. Not sure about everything else

  # confirm running
  sudo systemctl status libvirtd.service

  sudo virsh net-start default
  sudo virsh net-autostart default
  sudo virsh net-list --all
  # confirm output is default active yes yes

  # Give your user permission so that you can manage the server remotely using your SSH credentials
  sudo usermod -aG libvirt,libvirt-qemu,kvm,input,disk $USER


Remote configuration with virt-manager
-------------------------------------------

Once you have the server setup and running QEMU, you will want to manage it from virt-manager remotely.

.. code-block:: shell

  sudo apt-get install -y virt-manager
  # run the program
  virt-manager

Now that you have virt manager running, assuming you are running virt-manager on a machine other than the machine running QEMU,
go ahead and log into the machine running QEMU with your SSH credentials (username and host of remote machine).

Start creating a new virtual machine. In the first step give it the path to the ISO location on the server.
Configure the settings as you please and you can eventually launch it.
It should pop up a sceen showing the virtual machine's screen.

Configuration for a Windows VM
-----------------------------------

If you have configured a Windows VM, you may need to do a couple of things.

Internet Access
^^^^^^^^^^^^^^^^^

https://superuser.com/a/1689378

https://access.redhat.com/articles/2470791

https://github.com/virtio-win/virtio-win-pkg-scripts/blob/master/README.md

Most importantly, after following that, you want to change your NIC driver to ``virtio`` in virt-manager.

More Guest Tools
^^^^^^^^^^^^^^^^^^^^^

.. note::

  SPICE may be installed by the ``virtio-win-quest-tools.exe`` installation.

Go to https://www.spice-space.org/download.html then go to its Guest section to download Windows binaries for spice-guest-tools.
SPICE can help with a bunch of things such as 3D acceleration, clipboard sharing, etc.

