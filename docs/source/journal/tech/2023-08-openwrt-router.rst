August 2023 Setting up OpenWrt on old Router
===============================================

August 8 - Choosing an old router to use as a repeater with LAN port
------------------------------------------------------------------------

I recently ran Ethernet in my parents house to get more of our devices wired up, specifically to help connectivity with the streaming box we use.
It helped a lot, but we still need a "wired" connection up stairs. Really, it doesn't need to be truly wired, the device just needs to not use its on-board WiFi.
I have 3 older routers, all with `OpenWrt support <https://openwrt.org/supported_devices>`_.

* Linksys E1000 (Cisco E1000)

  * https://openwrt.org/toh/linksys/e1000

    * Insufficient resources and support ended in 2022

  * I believe I have the v1 revision.

* Netgear WNR1000 v2

  * https://openwrt.org/toh/netgear/wnr1000_v2

    * Insufficient resources and support ended in 2022

* Netgear WNDR3400 v3

  * https://openwrt.org/toh/netgear/wndr3400

    * Limited OpenWrt support
    * Does not have WiFi support
    * Does not have USB support
    * **Still has support :)**

\**Some time passes*\*

Netgear WNDR3400 v3
---------------------------------

I bricked my Netgear WNDR3400 v3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Was following the install instructions and accidentally unplugged power while I was flashing OpenWrt firmware.
Turns out I wasn't using the right barrel connector.
I made the right cable.
I had to set a static IP and can now ping ``192.168.1.1``, but I can't navigate to its web page.
When powering it on, the power light goes from orange, to blinking yellowish green.
I imagine that's not what is supposed to happen, as the orange light seemed to indicate healthiness before I flashed OpenWrt.
I think if I want to fix this, I need to do some sort of `recovery <https://openwrt.org/docs/guide-user/troubleshooting/vendor_specific_rescue>`_.

Let's give `jclehner/nmrpflash <https://github.com/jclehner/nmrpflash>`_ a try to unbrick this.

.. code-block:: console

  lavender@lavender-hp:~/bin$ nmrpflash --help
  nmrpflash: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34' not found (required by nmrpflash)

OK, so I did some research and I can't figure out what I need to do to make it work on my Ubuntu 20.04 install.
I was going to install from source, but I actually want to install with brew since that's an option. I need to quickly mark some packages as auto installed, then autoremove them.

.. code-block:: console

  lavender@lavender-hp:~/Documents/Clones/nmrpflash$ sudo apt-mark auto libpcap-dev libnl-3-dev libnl-route-3-dev && sudo apt autoremove

I'm going to try using brew to install with a simple ``brew install nmrpflash``.
And the install worked!

.. code-block:: console

  lavender@lavender-hp:~$ nmrpflash -L
  eno1             192.168.1.20     00:00:00:00:00:00
  wlo1             192.168.3.60     00:00:00:00:00:00
  lavender@lavender-hp:~$ sudo /home/linuxbrew/.linuxbrew/bin/nmrpflash -i eno1 -f ~/Downloads/openwrt-22.03.5-bcm47xx-mips74k-netgear_wndr3400-v3-squashfs.chk
  Waiting for Ethernet connection (Ctrl-C to skip).
  Advertising NMRP server on eno1 ... |
  Received configuration request from c0:ff:d4:98:be:85.
  Sending configuration: 10.164.183.253/24.
  Received upload request without filename.
  Uploading openwrt-22.03.5-bcm47xx-mips74k-netgear_wndr3400-v3-squashfs.chk ... OK (6164538 b)
  Waiting for remote to respond.
  Received keep-alive request (5).
  Remote finished. Closing connection.
  Reboot your device now.
  lavender@lavender-hp:~$

The status lights are different! Which is good I think...
It's not giving me an IP over DHCP, so let's try static again.
I'm in!

.. figure:: /images/2023-08-08-openwrt-login.png
  :width: 500px

I successfully logged in with root:admin.

Configuring
^^^^^^^^^^^^^

I now realize that no WiFi support means that this router likely can't even act as something that receives WiFi and then bridges the LAN ports.
Eh, I'm this far in, let's give it a try anyway. Worse case scenario, this becomes an unmanaged switch, or a managed switch to put somewhere else in my network.

I started following https://openwrt.org/docs/guide-user/network/wifi/relay_configuration.
It wants me to put the router on a different subnet and disable a few things.
Can do. I also found that you HAVE to have an IP of ``192.168.2.10`` after making these changes.
