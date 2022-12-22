VirtualBox
===========

VirtualBox is an awesome piece of software. The goal of this tutorial is to run it headless and use phpVirtualBox
to expose a web interface to configure VirtualBox.

This tutorial uses :docker-hub:`jazzdd/phpvirtualbox`, :docker-hub:`jazzdd/vboxwebsrv` and `VirtualBox <https://www.virtualbox.org>`_.


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
After installing, you can run ``/sbin/vboxconfig`` to confirm it's running without issue.


Installing phpVirtualBox and vboxwebsrv
------------------------------------------

We will install phpVirtualBox and vboxwebsrv using a single ``docker-compose.yml`` file.
However, first we must create a user with an SSH login that is in the ``vboxusers`` group.

.. code-block:: shell

  # Confirm that we have not already created a user in this group:
  getent group vboxusers
  useradd --create-home --system --groups vboxusers --shell /bin/false --user-group vbox
  mkdir /home/vbox/.ssh
  touch /home/vbox/.ssh/authorized_keys
  chown -R vbox:vbox /home/vbox/.ssh
  chmod 700 /home/vbox/.ssh
  chmod 600 /home/vbox/.ssh/authorized_keys

Now that you have the user set up, you are ready to configure the container

.. code-block:: shell

  cd /opt/containers
  mkdir phpvirtualbox
  cd phpvirtualbox
  mkdir ssh
  ssh-keygen -t rsa -N "" -f ssh/id_rsa
  cat ssh/id_rsa.pub | sudo tee /home/vbox/.ssh/authorized_keys

  # Store password in web_password.txt, and write that same password to a variable in .env to use in our docker-compose.yml file
  pwgen -N 1 -s 96 | sudo tee web_password.txt | awk '{ print "PASSWORD=" $0; }' | sudo tee -a .env

  vboxwebsrv --host 172.17.0.1 --port 18083 --passwordfile web_password.txt

Now you can edit ``docker-compose.yml``:

.. code-block:: yaml

  version: "3"

  services:
  #  vboxwebsrv:
  #    image: jazzdd/vboxwebsrv
  #    command: vbox@172.17.0.1
  #    restart: unless-stopped
  #    volumes:
  #      - "./ssh:/root/.ssh"
  #    environment:
  #      USE_KEY: 1
  #      # Inject an argument into the command since it is not quoted
  #      #SSH_PORT: "22 -o StrictHostKeyChecking=accept-new"
    phpvirtualbox:
      image: jazzdd/phpvirtualbox
      container_name: phpvirtualbox
      restart: unless-stopped
  #    depends_on:
  #      - vboxwebsrv
      # expose port 80 here if needed
      environment:
        SRV1_HOSTPORT: "172.17.0.1:18083"
        SRV1_NAME: "Server1"
        SRV1_USER: "user1"
        SRV1_PW: $PASSWORD
        CONF_browserRestrictFolders: "/home,/usr/lib/virtualbox"
        CONF_noAuth: "true"

  # Optionally include this if you specify the DOCKER_MY_NETWORK inside of your .env file
  networks:
    default:
      name: $DOCKER_MY_NETWORK


