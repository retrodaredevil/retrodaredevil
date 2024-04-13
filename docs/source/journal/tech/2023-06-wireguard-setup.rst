.. _wireguard_setup:

June 2023 WireGuard setup
======================================

June 12 - My SSH Tunnel VPN Thing Broke
------------------------------------------

I've been using SSH as a sort of VPN for essentially allowing myself to be on a few different local networks at once.
All my traffic is routed normally unless it's a 192.168.X.X address.
After messing with it and trying to make shork the computer that is used as the "host",
I couldn't get it to work again even after switching back to parker.
I'm sure it's just some small thing that I changed that I can't find, so oh well.
Really, I need to set up a real VPN anyway. I'm sure there are better solutions than SSH.

Setting up Wireguard Server Using Docker
-------------------------------------------

I started this on June 12 and continued and finished it on June 16.

I've heard good things about `Wireguard <https://www.wireguard.com/>`_, so I think I'll try and see how to set that up.
Luckily linuxserver.io has a `wireguard docker image <https://docs.linuxserver.io/images/docker-wireguard>`_ to use.
I was able to get server mode working with this compose file:

.. code-block:: yaml

  services:
    wireguard:
      image: lscr.io/linuxserver/wireguard:latest
      container_name: wireguard
      cap_add:
        - NET_ADMIN
      environment:
        - PUID=2000
        - PGID=2000
        - TZ=America/Chicago
        - SERVERURL=retrodaredevil.duckdns.org # this is optional, but I'm setting it because my IP changes
        - PERSISTENTKEEPALIVE_PEERS=all # this is optional, but recommended for a rotating IP
        # https://docs.linuxserver.io/images/docker-wireguard#server-mode
        - PEERS=4 # this makes this container be in server mode
      volumes:
        - /opt/containers/wireguard/config:/config
      ports:
        - 51820:51820/udp
      sysctls:
        - net.ipv4.conf.all.src_valid_mark=1
      restart: unless-stopped

I see that the PNG file containing the QR code is located in ``/opt/containers/wireguard/config/peer1/peer1.png``.
I need to do an rsync, but I need sudo permissions.
I could just move the file with sudo, but I'm actually going to allow ``sudo rsync`` to be used without a password.
First, I run ``which rsync`` to see rsync is located in ``/usr/bin/rsync``.
I now edit ``/etc/sudoers`` with ``sudo visudo /etc/sudoers`` and add ``lavender ALL=NOPASSWD:/usr/bin/rsync``.
Now on this laptop I can run this:

.. code-block:: shell

  rsync --rsync-path="sudo rsync" remote-shork:/opt/containers/wireguard/config/peer1/peer1.png ~/Downloads/peer1.png
  xdg-open ~/Downloads/peer1.png

.. note::

  I also debated looking for a program to view the image in a terminal: https://askubuntu.com/a/698064/756467

Awesome! Now I just need to open port 81820 on my router and I should be good to go.
(I just used ``ssh -D 8182 -N remote-shork`` and that seemed to work, so I must have a problem with redsocks or something in my SSH forward thing).
I'm gonna test this with the Wireguard Android app.
My phone no longer seems to have internet. I can confirm that it is receiving data, and if I stop the container, it stops receiving data.
So I must have to fix some sort of problem.

I did some research, and nothing seems worth trying, so I'm gonna follow this video: https://www.youtube.com/watch?v=GZRTnP4lyuo&t=333s.
I had commented ``SYS_MODULE`` and the ``/lib/modules`` volume, but most people seem to be setting it.
I do not believe these make a difference, but I'm going to include them anyway.
The video shows running ``wg`` inside the container, which I can run with my helper command ``compose-exec wg``.
The connected client shows this:

.. code-block::

  peer: *redacted*/*redacted*
    preshared key: (hidden)
    endpoint: 98.97.35.32:21169
    allowed ips: 10.13.13.2/32
    latest handshake: 1 minute, 15 seconds ago
    transfer: 15.93 KiB received, 7.28 KiB sent
    persistent keepalive: every 25 seconds

Everything seems correct and seems to be similar to what was shown in the video.
I am now suspecting that runningthis inside Docker inside a Linux Container on a Proxmox host may be the cause.
Looking at `these Reddit comments <https://www.reddit.com/r/Proxmox/comments/rufmvy/problem_with_wireguard_in_proxmox_lxc_container/>`_
I understand that some people had problems with loading the kernel module,
but I have a new enough install that I don't have to worry about that. Plus the logs seemed fine and said the module loaded fine.
(Maybe I really don't need the ``/lib/modules`` stuff - I do get this... so yeah: ``As the wireguard module is already active you can remove the SYS_MODULE capability from your container run/compose.``).
The comments do talk about having the ``nesting`` and ``keyctl`` features, but I already have ``nesting`` and ``mknod``,
so maybe I need to add ``keyctl``.
I don't feel like trying that.

Maybe my phone was being dumb. I'll try to use Wireguard on my laptop.
I've installed wireguard on my laptop via apt with ``sudo apt install -y wireguard resolvconf``.
Now I put my ``peer2.conf`` into ``/etc/wireguard/wg0.conf`` on my laptop.

Alright, this is too much of a pain in the ass to setup on bare metal.
Let's try this: https://docs.linuxserver.io/images/docker-wireguard#client-mode.
That's better. Now I get this output:

.. code-block::

  Uname info: Linux c1238d7ac3c0 5.4.0-150-generic #167-Ubuntu SMP Mon May 15 17:35:05 UTC 2023 x86_64 GNU/Linux
  **** It seems the wireguard module is already active. Skipping kernel header install and module compilation. ****
  **** As the wireguard module is already active you can remove the SYS_MODULE capability from your container run/compose. ****
  **** Client mode selected. ****
  [custom-init] No custom files found, skipping...
  **** Disabling CoreDNS ****
  Warning: `/config/wg0.conf' is world accessible
  [#] ip link add wg0 type wireguard
  [#] wg setconf wg0 /dev/fd/63
  [#] ip -4 address add 10.13.13.3 dev wg0
  [#] ip link set mtu 1420 up dev wg0
  [#] resolvconf -a wg0 -m 0 -x
  [#] wg set wg0 fwmark 51820
  [#] ip -6 route add ::/0 dev wg0 table 51820
  Error: IPv6 is disabled on nexthop device.
  [#] resolvconf -d wg0 -f
  [#] ip link delete dev wg0
  s6-rc: warning: unable to start service svc-wireguard: command exited 2

I couldn't find much about that last line, but I was linked to (an unrelated) thread here: https://discourse.linuxserver.io/t/wireguard-error/7409.
It seems that running this Linuxserver image inside Docker inside LXC inside Proxmox is discouraged.

*Tangent* Alright now I found a place that says I need ``keyctl``: https://www.reddit.com/r/Proxmox/comments/oitudd/has_anyone_found_a_solution_for_docker_in_lxc_for/.
Tried that and it didn't work change anything, so I now have it disabled again.

I now disabled IPv6 in my locally running Wireguard client connects to the server just fine,
but when I go inside my container, I see that none of its packets are reaching the Internet or even my server's local network.
I'm now convinced that something is up with the configuration of my server, likely related to the whole Docker inside of... yeah you get it.

Worth noting that I want to check out this link whenever r/WireGuard comes back from the blackout: https://www.reddit.com/r/WireGuard/comments/zkisej/wireguard_in_proxmox_lxc_container/.

Setting up Wireguard in LXC Directly
------------------------------------

So I couldn't get Wireguard inside my Docker container to work, but luckily there's a helper script to create a LXC for me (https://tteck.github.io/Proxmox/).
For the name of the container, I will use ``shoal``, which is a large school of fish (thanks ChatGPT).
I edited ``/etc/pivpn/wireguard/setupVars.conf`` on shoal to update my host to be my domain and I also made the DNS point to betta (my AdGuard Home container).

I now run these:

.. code-block:: 

  pivpn add
  pivpn -qr

Holy crap it works. I got my phone connected and it just works.
Well, that was easy. Should have tried this first I guess.

Summary
-----------

I should have used the helper script right off the bat.
The fact that so many people had problems with Docker on LXC on Proxmox makes me wonder if I should create a VM
just to do stuff like this. I mean, I can still have my LXC, but maybe some things would just run better inside Docker on a VM.

This was a good experience I learned a lot of stuff, but it was frustrating to not really solve my problems with the linuxserver image on Docker on LXC on Proxmox.

Continuing
-------------

I am currently able to connect on my phone.
I found that changing allowed IPs on my phone to ``10.6.0.0/32, 192.168.3.0/24`` made it so only requests to the local network went through the VPN.
This means that I can keep my VPN on all the time on my phone and access my local network.
Now I just have to do this on my laptop.

.. note:: 

  I believe there is configuration I could do on the server to make the generated configurations only route local network packets by default,
  but that's easy enough to configure myself.

I had luck getting the linuxserver docker image to be used as a client, but I don't know how to get my host machine to use it.
Let's try the bare metal install again.
Last time my problem was resolvconf messing up DNS stuff.
I found `this SO link <https://superuser.com/questions/1500691/usr-bin-wg-quick-line-31-resolvconf-command-not-found-wireguard-debian>`_
which recommended I instead install ``openresolv``, and now ``which resolvconf`` works and my DNS seems to also work!
Now we're back to editing ``/etc/wireguard/wg0.conf`` on my laptop.
I'll quickly get the conf file from my wireguard LXC.
I'll change ``AllowedIPs`` to ``10.6.0.0/32, 192.168.3.0/24`` again.
Now I can run ``wg-quick up wg0``. Now I can run ``sudo wg`` to confirm it's working. And it is!
I now have a consistent connection to my server's local network!
