October 2023 New Laptop
====================

https://www.microcenter.com/product/663735/lenovo-legion-pro-5-16-gaming-laptop-computer-platinum-collection-onyx-grey

October 7 - Installing OS
-------------------------

I'm installing Pop!_OS on a new laptop.
I want my drive to be encrypted, so I had to do the clean install, which wiped my disk completely but setup encryption.
Now after the install I can resize it to my liking!
I found a tutorial (https://mutschler.dev/linux/pop-os-btrfs-22-04/) which does some more advanced stuff than I needed, but it looks helpful.

Turns out, that tutorial is doing wayy more than I need.
I opted to stick with the clean install of Pop!_OS, but decrypting (almost) the entire SSD whenever my computer boots up took literal minutes.
I don't feel like it should take that long, but even if it took 30 seconds, that would not be something I want to put up with.
Alright. Let's do this install again.

I could do a clean (unencrypted) install, but now that there's no downside to doing a manual install, I will opt for that.
Now that I see what sizes the default install gave partitions, I will note them here

* Boot: 1022 MiB
* recovery: 4 GiB
* Encrypted root: 944.87 GiB
* Swap: 4 GiB

I'll keep the boot and recovery drives (although I'll still check the reformat box). I'll create a root partition that's pretty big.
I'll create the swap, and I'll go ahead and create an unused ext4 partition that I will encrypt later.
The leftover unused space will be used for a Windows install.

Now that everything is working in my Pop!_OS install, it's time to create bootable Windows media.
I'm going to use `WoeUSB <https://github.com/WoeUSB/WoeUSB/releases/tag/v5.2.4>`_ for this.
I try running it, and it complains about ``wimlib-imagex`` not being available in the path.
A ``sudo apt install wimtools`` does the trick to fix the problem.
Now I make sure my USB drive is ``/dev/sda`` and then run ``sudo bash Downloads/woeusb-5.2.4.bash --device Downloads/Win11_22H2_English_x64v2.iso /dev/sda``.

Pop!_OS Setup
----------------------

May be similar to: https://gist.github.com/retrodaredevil/def6d23a03d9e46683933ef0c017d96c

* Install:

  * ``sudo apt install -y net-tools vim-gtk iputils-tracepath traceroute curl wget git netcat-openbsd tmux tree man-db file xsel htop gpg-agent rsync pwgen``
  * https://www.jetbrains.com/toolbox-app/download
  * https://discord.com/download
  * RGB Keyboard Control: https://github.com/4JX/L5P-Keyboard-RGB
  * Minecraft: https://www.minecraft.net/en-us/download
  * Cheese: ``sudo apt install cheese``

* Add SSH key: https://github.com/settings/keys
* Clone programming repo (https://github.com/retrodaredevil/programming)
* Install `GNOME Tweaks <https://pop-os.github.io/docs/customize-pop/gnome-tweaks-extensions/gnome-tweaks.html>`_ by running ``sudo apt install gnome-tweaks``

  * Launch the Tweaks application, Keyboard & Mouse > Additional Layout Options > Make Caps Lock an additional Esc
  * Restart IntelliJ if you have it open

Git Signing Key
^^^^^^^^^^^^^^^

I have git version 2.34.1, so that means I can use my SSH key as my signing key if I would like.
Normally, my ``.gitconfig`` looks like this:

.. code-block::

  [user]
    name = Lavender Shannon
    signingkey = E274ED307902B127
  [includeIf "gitdir/i:~/programming/"]
    path = ~/programming/.gitconfig-default
  [includeIf "gitdir:~/programming/.git/modules/Mst/"]
    path = ~/programming/Mst/.gitconfig-mst

  [filter "lfs"]
    clean = git-lfs clean -- %f
    smudge = git-lfs smudge -- %f
    process = git-lfs filter-process
    required = true

  [commit]
    gpgSign = true
  [tag]
    gpgSign = true

However, now I can instead follow this tutorial: https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key

.. code-block:: shell

  git config --global gpg.format ssh
  git config --global user.signingkey /home/lavender/.ssh/id_rsa.pub

Now my ``.gitconfig`` looks like this:

.. code-block::


  [user]
    name = Lavender Shannon
    signingkey = /home/lavender/.ssh/id_rsa.pub
  [gpg]
    format = ssh

  [includeIf "gitdir/i:~/programming/"]
    path = ~/programming/.gitconfig-default
  [includeIf "gitdir:~/programming/.git/modules/Mst/"]
    path = ~/programming/Mst/.gitconfig-mst

  [filter "lfs"]
    clean = git-lfs clean -- %f
    smudge = git-lfs smudge -- %f
    process = git-lfs filter-process
    required = true

  [commit]
    gpgSign = true
  [tag]
    gpgSign = true

Perfect! That was super easy! Now I make sure to add the key to my GitHub (and school GitLab) as a signing key.
