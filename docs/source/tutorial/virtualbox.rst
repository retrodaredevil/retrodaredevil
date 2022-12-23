VirtualBox
===========

VirtualBox is an awesome piece of software. The goal of this tutorial is to run it headless and use phpVirtualBox
to expose a web interface to configure VirtualBox.

This tutorial uses `VirtualBox <https://www.virtualbox.org>`_.


Installing VirtualBox
-----------------------

VirtualBox is a difficult piece of software to put in a Docker container. (It is possible: https://www.cbtechinc.com/headless-virtualbox-docker/).
Because of the difficulty, I find it easier to install on the host system and use it uncontainerized.
Go to https://www.virtualbox.org/wiki/Linux_Downloads to find the latest release.

Before installing, we must do one of two things: Install VirtualBox's dependencies manually, or install ``gdebi`` to help us install its depdencies:

.. code-block:: shell

  cd ~/Downloads
  wget https://download.virtualbox.org/virtualbox/7.0.4/virtualbox-7.0_7.0.4-154605~Debian~bullseye_amd64.deb

  sudo apt-get update && sudo apt-get install -y gdebi-core
  # gdebi helps us install dependencies required by the .deb file
  sudo gdebi virtualbox-7.0_7.0.4-154605~Debian~bullseye_amd64.deb

.. note::

  For future reference for myself, the packages that were needed are: (Most people can ignore this)

  Requires the installation of the following packages: libdouble-conversion3 libegl-mesa0 libegl1 libevdev2 libgudev-1.0-0 libinput-bin libinput10 libmd4c0 libmtdev1 
  libpcre2-16-0 libqt5core5a libqt5dbus5 libqt5gui5 libqt5help5 libqt5network5 libqt5opengl5 libqt5printsupport5 libqt5sql5 libqt5sql5-sqlite libqt5svg5 libqt5widgets5 
  libqt5x11extras5 libqt5xml5 libwacom-bin libwacom-common libwacom2 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-util1 libxcb-xinerama0 
  libxcb-xinput0 libxcb-xkb1 libxkbcommon-x11-0 qt5-gtk-platformtheme qttranslations5-l10n

After installation, there will likely be error messages telling you to install linux-headers.
In my case I ran: ``sudo apt-get install -y linux-headers-amd64 linux-headers-5.10.0-19-amd64``.
After installing, you can run ``sudo /sbin/vboxconfig`` to confirm it's running without issue.

Installing VirtualBox Extension pack
---------------------------------------

Pretty much everything we are going to do after this requires the extension pack, so let's install it now:

.. code-block:: shell

  cd ~/Downloads
  # Find your version here: https://www.virtualbox.org/wiki/Downloads (make sure it matches the version you have installed)
  wget https://download.virtualbox.org/virtualbox/7.0.4/Oracle_VM_VirtualBox_Extension_Pack-7.0.4.vbox-extpack
  sudo vboxmanage extpack install Oracle_VM_VirtualBox_Extension_Pack-7.0.4.vbox-extpack


Running the vboxwebsrv daemon
-------------------------------

VirtualBox is installed on our system, but in order for tools other than the command line interface to interact with VirtualBox,
we need to get this daemon up and running.
The installation of VirtualBox along with the extension pack should have created a ``vboxusers`` group 
and a systemd service file to run ``vboxwebsrv`` for us.
Although there is a service already created to run ``vboxwebsrv``, it has not yet been fully configured,
and the above installation did not even create a user to be used!
The offical documentation for this can be found here: https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/vboxwebsrv-daemon.html


.. code-block:: shell

  # Confirm that we have not already created a user in this group:
  getent group vboxusers
  useradd --create-home --system --gid vboxusers --groups shadow --shell /bin/false vbox
  passwd -L vbox
  #mkdir /home/vbox/.ssh
  #touch /home/vbox/.ssh/authorized_keys
  #chown -R vbox:vbox /home/vbox/.ssh
  #chmod 700 /home/vbox/.ssh
  #chmod 600 /home/vbox/.ssh/authorized_keys
  systemctl stop vboxweb-service
  systemctl disable vboxweb-service

We have just disabled vboxweb-service which is configured upon VirtualBox installation.
You can reenable it later if you need to for some reason, but I found it hard to understand.
Paste these contents in ``/etc/systemd/system/vboxweb.service``.

.. code-block::

  [Unit]
  Description=VirtualBox Web Service
  After=network.target

  [Service]
  User=vbox
  Group=vboxusers
  ExecStart=/usr/bin/vboxwebsrv --pidfile /home/vbox/vboxweb.pid --host=0.0.0.0

  [Install]
  WantedBy=multi-user.target

After pasting the contents and saving the file, reload systemctl with ``sudo systemctl daemon-reload``.
Now, start the service with ``sudo systemctl start vboxweb``.



Managing VMs with RemoteBox
-------------------------------

There are many ways to manage VirtualBox VMs after installing VirtualBox.
You can opt to use terminal commands, or use phpVirtualBox if you are running an old version of VirtualBox.
RemoteBox is kept up to date, which is why I recommend it.

You can view system requirements here: https://remotebox.knobgoblin.org.uk/?page=installubuntu
and download it here: https://remotebox.knobgoblin.org.uk/?page=downloads.
In my case I ran this on my client system:

.. code-block:: shell

  cd ~/bin
  mkdir RemoteBox && cd RemoteBox
  wget https://remotebox.knobgoblin.org.uk/downloads/RemoteBox-3.2.tar.bz2
  sudo apt-get install libgtk3-perl libsoap-lite-perl freerdp2-x11 tigervnc-viewer 
  # ... tar -xf ...

To login, use the credentials of any linux user on the system. Since we allow the ``vbox`` user to access the ``/etc/shadow`` file,
that is the default authentication method used by vboxwebsrv.

.. note:: 

  On Linux, the name of the default authentication module is VBoxAuth.
  Another option is VBoxAuthSimple, which requires some extra configuration described here: https://www.virtualbox.org/manual/ch07.html#vbox-auth

Now you can create VMs at will. I find it easiest to download an ISO online and place it in the ``/home/vbox/Downloads`` directory.
Add that file to a create VM's IDE storage drive.
At this point, you can either start the VM now and configure it, or start it after configuring RDP.
VirtualBox itself should launch a xfreerdp instance.

Once a VM is created, we want to enable the ability to connect to it via RDP (this can allow guacamole to access it or any other RDP client).
If you are not using Guacamole, Remmina is a good choice that runs locally.
To configure a VM's RDP, click on the VM, go to its settings, then go to Display>Remote Display and enable RDP.
Set the port range to "3389" instead of "3389-4389".
Set the Authentication to "External". This allows you to use the login credentials of any users on the computer.



Uninstalling VirtualBox
-------------------------

In case you need to uninstall VirtualBox for some reason:


.. code-block:: shell

  apt-get purge virtualbox*
  apt-get autoremove
  groupdel vboxusers
  groupdel vboxsf
  userdel vbox
  rm -rf /home/vbox  # note this command may have unintended consequences if you have data in /home/vbox that you want to keep
  rm -rf /usr/lib/virtualbox/
