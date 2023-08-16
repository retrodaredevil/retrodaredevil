August 2023 OPNsense in Proxmox
=================================

This page contains a journal I wrote while setting up OPNsense inside of Proxmox.

August 14 - Choosing Routing Software
---------------------------------------

I recently setup spiderverse (formerly parker) with Proxmox 8.
This computer will live in my dorm room, and I want to have it be in control of being my router.
I want to decide between `OPNsense <https://opnsense.org/>`_ (`gh <https://github.com/opnsense/core>`__), `pfSense <https://www.pfsense.org/>`_ (`gh <https://github.com/pfsense/pfsense>`__), and `OpenWrt <https://openwrt.org/>`_ (`gh <https://github.com/openwrt/openwrt>`__).
OK, I think I'll go ahead and rule out OpenWrt, as I want something more powerful.

With a little bit of research, I see that OPNsense and pfSense are fairly similar, but pfSense is more popular and has been around longer.
I get the feeling that OPNsense is a little more "cool", and possibly slightly easier to configure and understand.
Overall, this tutorial: https://teklager.se/en/pfsense-vs-opnsense/ has convinced me that OPNsense is the way to go.

Creating an OPNsense VM
-------------------------

I'm following https://homenetworkguy.com/how-to/run-opnsense-in-proxmox-vm/.

I first need to download am image from https://opnsense.org/download/.
I grab the DVD ISO image and upload it to spiderverse's ISO images inside its local storage.
Now that I have the ``OPNsense-23.7-dvd-amd64.iso`` uploaded, it's time to create a VM!
I will name this ``super-collider`` and give it an ID of 200, as I want to reserve the 1XX IDs for the existing containers/VMs on bigger-fish.
I chose what the tutorial recommends and give it all 4 cores of my machine (``lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('``).
8GB of RAM should be good.
For networks I'll leave it as the default bridge for now, but I will have to come back and add more networks.
The tutorial recommends I create a bridge for each physical port.
This means that I get to leave the network I'm currently configuring un-altered, as it will be the bridge for the port that I'm designating as my WAN port.

.. figure:: /images/2023-08-14-proxmox-create-opnsense-vm-confirm.png
  :width: 100%

I'll go ahead and create some network bridges following the naming conventions listed on `Network Configuration <https://pve.proxmox.com/wiki/Network_Configuration>`_.
``vmbr1`` gets ``enp2s0f0`` as its only bridge port, and ``vmbr2`` gets ``enp2s0f1`` as its only bridge port.
I add them in the Hardware tab of my VM, and once I'm done I have a total of 3 network devices added.
Now I can start the VM!

Configuring OPNsense
---------------------

I booted into the installer and skipped the manual assignment and let it auto assign stuff.
Hopefully that's OK. I'll just assume it's fine for now and continue on by logging in with installer/opnsense.
The `OPNsense Installer docs <https://docs.opnsense.org/manual/install.html#opnsense-installer>`_ say ZFS is usually the best option, so I will choose that.
It gives me the option of a RAID, but I won't do that here. If I really wanted to have a RAID setup, I would have configured by local-lvm to be backed by a RAID.
I choose the ``stripe`` option. I choose the option to reboot.

Now I stop the VM before it boots into the installation again. I remove the install media by editing the CD/DVD Drive.
Now I start it again.
I take a look at the output of ``ifconfig`` and notice that ``vtnet0`` is my LAN for OPNsense,
which happens to be using the ``vmbr0``. I definitely need to change that to be my WAN, as that's the Ethernet port that is being used to connect this to my network!
Remember, I don't want this to be a router for my current network. I just want to configure it as a router while it's on this network.
Now I go into the ``1) Assign interfaces`` option, and it asks me questions that are shown in the tutorial.
I'll make ``vtnet0`` the WAN for now, as I do want the Ethernet port its connected to now to be the WAN port.
Now I have this:

.. code-block::

  WAN -> vtnet0
  LAN -> vtnet1
  OPT1 -> vtnet2

After confirming the WAN correctly shows ``192.168.3.109/24``.
My router sees that IP address as being my ``OPNsense`` host, which is good.
I am able to use option ``7) Ping host`` to ping my phone, so that's good.
I'm going to start following the tutorial again. I will choose ``2) Set interface IP address``.
I'll configure the LAN, y for ``Configure IPv4 address LAN interface via DHCP``,
n for ``WAN tracking``, n for ``DHCP6``.
My ``DHCP6`` option differs from the tutorial because I don't want to use IPv6 at all.
Now I keep the remaining defaults.

Currently my LAN IP is ``192.168.1.102``, which I believe was assigned by OPNsense, as that's the only logical thing that could have a DHCP server to give out an IP.
I mean, OPNsense's LAN network currently isn't connected to anything.
If I was on its LAN, I should be able to access the web interface, but I am not.
`This forum post <https://forum.opnsense.org/index.php?topic=573.0>`_ says to make a NAT so that I can access it from the local network I am currently on.
The `Port forwarding docs <https://docs.opnsense.org/manual/nat.html#port-forwarding>`_ don't seem to show how to do this from the command line,
so I guess I'll go connect my computer to spiderverse via Ethernet to make this change.

August 15 - Port Forwarding the GUI
-----------------------------------

Did some playing around. When I do ``2) Set interface IP address``, I needed to configure the LAN to not get its address from DHCP.
Instead, give it an IP address of 192.168.1.1 and a subnet count of 24, then I enable DHCP on the LAN.
I have my computer plugged into Ethernet and after making these changes, my computer is given an IP address from the DHCP server!
I now know that the bottom port is port 0, which currently corresponds to vtnet1.
I tried going to 192.168.1.1 in my browser, but it didn't work. I press enter inside the console and the IP address is back at 192.168.1.102.
Interesting...
Well, I go to that and I see the web interface! Success! I guess?
I login with root/lavenders_password_here and I'm good to go.
Continuing with defaults for everything and I notice "Block RFC1918 Private Networks".
Let's disable this, as I currently want to be able to access it on my private network!
I also think that having this disabled might be necessary when this is on the school's network,
as MyResNet attempts to give you your very own LAN (I say attempts because I'm not convinced that it works half the time).
Eventually it prompts me to set 192.168.1.1 as the LAN network address, which I confirm.
It says it will reload the dashboard when it is done, but it doesn't and I manually go to 192.168.1.1.
Yay! Now I can finally configure this knowing everything is setup.

Now I have got port forwarding working with this:

.. figure:: /images/2023-08-15-opnsense-port-forward-443.png
  :width: 80%

Finally, I can configure it on my main LAN network!
