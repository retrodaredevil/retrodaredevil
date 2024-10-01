October 2023 New Laptop
========================

https://www.microcenter.com/product/663735/lenovo-legion-pro-5-16-gaming-laptop-computer-platinum-collection-onyx-grey

https://psref.lenovo.com/Detail/Legion_Pro_5_16IRX8?M=82WK0045US

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

.. note::

  (Update October 25) - I believe this took so long not because the drive was encrypted, but because I was likely using hybrid graphics at the time,
  which I will later discover is glitchy with NVIDIA graphics.

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

  * ``sudo apt install -y net-tools vim-gtk iputils-tracepath traceroute curl wget git netcat-openbsd tmux tree man-db file xsel htop gpg-agent rsync pwgen ipython3 gparted``
  * Setup flathub: ``flatpak remote-add flathub https://flathub.org/repo/flathub.flatpakrepo``
  * https://www.jetbrains.com/toolbox-app/download
  * https://discord.com/download (Alternatively install from Pop!_Shop)
  * RGB Keyboard Control: https://github.com/4JX/L5P-Keyboard-RGB
  * Minecraft: https://www.minecraft.net/en-us/download
  * Cheese: ``sudo apt install cheese``
  * Signal: https://signal.org/download (Alternatively install from Pop!_Shop)
  * Steam: From Pop!_Shop
  * DisplayLink drivers: https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
  * Plexamp: ``flatpak install --user --assumeyes flathub com.plexamp.Plexamp``
  * Pithos: ``flatpak install --user --assumeyes flathub io.github.Pithos`` https://pithos.github.io/#install
  * Chromium: ``flatpak install --user --assumeyes org.chromium.Chromium`` https://flathub.org/apps/org.chromium.Chromium
  * Zoom: ``flatpak install --user --assumeyes us.zoom.Zoom`` https://flathub.org/apps/us.zoom.Zoom
  * Docker: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
  * SDKMAN: ``curl -s "https://get.sdkman.io" | bash`` https://sdkman.io/install

    * ``sdk install java 21-tem``

  * VS Code: ``flatpak install --user --assumeyes com.visualstudio.code`` https://flathub.org/apps/com.visualstudio.code
  * Brew: https://docs.brew.sh/Homebrew-on-Linux

    * ``/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"``
    * ``sudo apt-get install build-essential``
    * ``echo 'export PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"' >> ~/.bashrc``
    * ``brew install mosh``

* Less essential install

  * Krita: ``flatpak install --user --assumeyes flathub org.kde.krita``
  * Kdenlive: ``flatpak install --user --assumeyes flathub org.kde.kdenlive``
  * ISO Image Writer: ``flatpak install --user --assumeyes flathub org.kde.isoimagewriter``
  * VLC: ``flatpak install --user --assumeyes flathub org.videolan.VLC``
  * FileZilla: ``flatpak install --user --assumeyes flathub org.filezillaproject.Filezilla``
  * Audacity: ``flatpak install --user --assumeyes flathub org.audacityteam.Audacity``
  * Plex: ``flatpak install --user --assumeyes flathub tv.plex.PlexHTPC && flatpak install --user --assumeyes flathub tv.plex.PlexDesktop``
  * Emulators

    * ``flatpak install --user --assumeyes flathub org.libretro.RetroArch``
    * ``flatpak install --user --assumeyes flathub org.DolphinEmu.dolphin-emu``
    * N64 emulator: ``flatpak install --user --assumeyes flathub io.github.gopher64.gopher64``
    * mGBA: ``flatpak install --user --assumeyes flathub io.mgba.mGBA``
    * 3DS emulator: ``flatpak install --user --assumeyes flathub org.citra_emu.citra``
    * Switch emulator: ``flatpak install --user --assumeyes flathub org.ryujinx.Ryujinx``

* Add SSH key: https://github.com/settings/keys
* Clone programming repo (https://github.com/retrodaredevil/programming)
* Install `GNOME Tweaks <https://pop-os.github.io/docs/customize-pop/gnome-tweaks-extensions/gnome-tweaks.html>`_ by running ``sudo apt install gnome-tweaks``

  * Launch the Tweaks application, Keyboard & Mouse > Additional Layout Options > Make Caps Lock an additional Esc
  * Restart IntelliJ if you have it open

* Remaps: Settings > Keyboard > Keyboard Shortcuts

  * Ctrl+Alt+T to Open Terminal

    *  Search "Launch Terminal" > Add another shortcut

* Isolate workspaces - Dock only shows windows on current workspace

  * ``gsettings set org.gnome.shell.extensions.dash-to-dock isolate-workspaces true`` (thanks https://askubuntu.com/questions/992558/how-can-i-configure-the-ubuntu-dock-to-show-windows-only-from-the-current-worksp#992559)

* Android Studio Setup

  * https://developer.android.com/studio/run/device
  * ``sudo usermod -aG plugdev $LOGNAME && sudo apt-get install -y android-sdk-platform-tools-common adb``

* IntelliJ Setup*

  * Disable Java Bytecode Decompiler Plugin (https://youtrack.jetbrains.com/issue/IDEA-198397/Allow-decompilation-to-be-cancelled)
  * Note that this does not seem to fix the issue I have of pasting text and then having IntelliJ freeze (only sometimes with a specific payload)


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

If I make a commit and then run ``git log --show-signature``, I get an error message of ``error: gpg.ssh.allowedSignersFile needs to be configured and exist for ssh signature verification``.
`This tutorial <https://blog.dbrgn.ch/2021/11/16/git-ssh-signatures/>`_ recommends that I create a file in ``~/.config/git/allowed_signers``.
I think I'll version control this file in my own location.
My ``allowed_signers`` file now looks like this:

.. code-block::

  retrodaredevil@gmail.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCzm7cjGRjnJYM65dxcBM83CMmEBWZ3QGcsw1fEIQ4J8ARynrKVCPGDXUDHmbgajxo79xxGDDS4+ZkX9Zia10ULejBbatxXaxH2NaxCNIYNHEdUrEOtGqsE105BT6qJS6QcWfdjPirw2Gz6EWJlxhUR6KOWau18o56krJ87QPrdYgd+iE6yzmHOGtpwkPo+3CNMAZaEwbcSKNPdOutwOAPqj9E/Fw8wUmZK5Ry9tJeIwH0zeM2y1ktfXz1Fgn3E1W3QZ0h6e1b4xJWT1yNVK+b6qB4icDkOxDNNLx4zZ5ylmFpwj0m8fr13MC4N+wBoJUlitjPHjit87asblKavh+a4Am0EbhkKVbC+vBl5X7SnCipeD8XJ3d7anZiLevTIXzmwQ7xwwriieJa8UYFJmYYaJweXyPqEhNm3M+E6fEM+aH8eNlKbkCag9whXdRV+Q31wpJolR53Nlg38KBLR6ZrPLETIfqbTkt/YDSTTfNMX7IvfYnH359Xhu81Z50OspAc= lavender@lavender-legion

It's just the public key with an email before it. Simple enough!

Windows Setup
---------------

I setup Windows 11 with a local account by attempting to sign in with the email no@thankyou.com. I was surprised at how well that worked.

* Install

  * Firefox: https://www.mozilla.org/en-US/firefox/new/
  * WinGet: https://learn.microsoft.com/en-us/windows/package-manager/winget/

    * https://apps.microsoft.com/detail/9NBLGGH4NNS1?hl=en-us&gl=US
    * winget repository: https://winstall.app
    * (Was already installed, just needed to be updated)

  * Git & Git Bash: https://git-scm.com/downloads

    * (In powershell) ``winget install --id Git.Git -e --source winget``
    * This does the default install, which is fine for me because it installs Git Bash too, and that's all I need

  * In Git bash:

    * ``winget install powertoys --source msstore``
    * ``winget install --id=Valve.Steam -e``
    * ``winget install --id=JetBrains.Toolbox -e``
    * ``winget install --id=EpicGames.EpicGamesLauncher -e``
    * ``winget install --id=OpenWhisperSystems.Signal -e``
    * ``winget install --id=Discord.Discord -e``
    * ``winget install --id=Mojang.MinecraftLauncher -e``
    * ``winget install --id=Plex.Plexamp -e``
    * ``winget install --id=Ubisoft.Connect  -e``

  * Find my drivers: https://www.nvidia.com/download/index.aspx?lang=en-us

    * Restart PC after doing this
    * Go to System > Display > Advanced display

      * Confirm internal display is at 240Hz

* Remap caps lock

  * PowerToys Settings > Keyboard Manager > Remap a key

* Make Minecraft use GPU

  * System > Display > Graphics
  * Add an app, find ``javaw`` in the Minecraft Launcher program files
  * javaw > Graphics preference > High performance

* Turn off tap to click

  * Settings -> Bluetooth and Devices -> Touchpad -> Taps - Turn all off

* IntelliJ

  * Set terminal to Git Bash

    * Settings -> Tools -> Terminal

* Epic Games Launcher

  * Disable notifications by going to Settings > Desktop Notifications

``.gitconfig`` in Windows
----------------------------

It's fairly similar to how I did it on linux, it's just slightly different.

.. code-block::

  [user]
    name = Lavender Shannon
    signingkey = /c/Users/lavender/.ssh/id_rsa.pub
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

Laggy External Display in Pop!_OS
------------------------------------

My external display is quite a bit more laggy than my internal one.
I'm running NVIDIA Graphics, but let's try hybrid mode (even though people seem to think that causes issues).
Hybrid graphics doesn't seem to change anything, but if I open NVIDIA Settings > GPU 0 > PowerMizer and set Preferred Mode to Maximum, it works!
(Thanks https://github.com/pop-os/pop/issues/2747#issuecomment-1371025332)

Screenshots in Pop!_OS
---------------------------

I'll be using the Print key to start to make my selection, then I save it and it shows up in recents.
I'll still have to play around with this.

Monitor Scaling in Pop!_OS
-----------------------------

Follow this to scale monitors individually: https://askubuntu.com/questions/1084069/how-to-set-different-scaling-on-multi-monitor-3-monitors

Lessons Learned in Buying this Laptop
---------------------------------------

* Don't get an NVIDIA GPU (Getting it to be not glitchy on Linux is a pain)
* Make sure there are some thunderbolt USB C ports. Also understand how a display connected via USB C interacts with the graphics card
* Understand if the HDMI port requires the GPU to be used

October 9 - About the NVIDIA graphics
---------------------------------------------------------------------

Hybrid mode is worse than NVIDIA Graphics for external monitors.
Don't use hybrid mode unless you don't plan on using an external monitor.

Here is the output of ``inxi -G`` when selecting Hybrid Graphics in Pop!_OS.
I believe it actually ends up being the same as when using NVIDIA Graphics mode.

.. code-block:: console

  lavender@lavender-legion:~$ inxi -G
  Graphics:
    Device-1: Intel driver: i915 v: kernel
    Device-2: NVIDIA driver: nvidia v: 535.113.01
    Device-3: Luxvisions Innotech Integrated Camera type: USB
      driver: uvcvideo
    Display: x11 server: X.Org v: 1.21.1.4 driver: X:
      loaded: modesetting,nvidia unloaded: fbdev,nouveau,vesa gpu: i915
      resolution: 1: 1920x1080~60Hz 2: 2560x1600~240Hz
    OpenGL: renderer: Mesa Intel Graphics (RPL-S)
      v: 4.6 Mesa 23.1.3-1pop0~1689084530~22.04~0618746

Here is the correct output of ``nvidia-smi`` indicating that things are using the GPU:


.. code-block:: console

  lavender@lavender-legion:~$ nvidia-smi
  Tue Oct 10 12:22:32 2023
  +---------------------------------------------------------------------------------------+
  | NVIDIA-SMI 535.113.01             Driver Version: 535.113.01   CUDA Version: 12.2     |
  |-----------------------------------------+----------------------+----------------------+
  | GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
  |                                         |                      |               MIG M. |
  |=========================================+======================+======================|
  |   0  NVIDIA GeForce RTX 4070 ...    Off | 00000000:01:00.0  On |                  N/A |
  | N/A   38C    P5               4W / 140W |    858MiB /  8188MiB |     41%      Default |
  |                                         |                      |                  N/A |
  +-----------------------------------------+----------------------+----------------------+

  +---------------------------------------------------------------------------------------+
  | Processes:                                                                            |
  |  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
  |        ID   ID                                                             Usage      |
  |=======================================================================================|
  |    0   N/A  N/A      2696      G   /usr/lib/xorg/Xorg                          487MiB |
  |    0   N/A  N/A      2999      G   /usr/bin/gnome-shell                         67MiB |
  |    0   N/A  N/A      4862      G   firefox                                     179MiB |
  |    0   N/A  N/A      5694      G   ...,WinRetrieveSuggestionsOnlyOnDemand       39MiB |
  |    0   N/A  N/A      9084      G   ...ures=SpareRendererForSitePerProcess       15MiB |
  |    0   N/A  N/A     16110      G   ...bian-installation/ubuntu12_32/steam        2MiB |
  |    0   N/A  N/A     16120      G   ...allation/ubuntu12_64/steamwebhelper        6MiB |
  |    0   N/A  N/A     29033      G   ...ures=SpareRendererForSitePerProcess        3MiB |
  +---------------------------------------------------------------------------------------+

Notice specifically that ``/usr/lib/xorg/Xorg`` is using more than 10MiB of memory.
If it is using something like 4MiB of memory, then it's not really using the GPU at all.

Enable Hibernation in Pop!_OS
-------------------------------------

At some point, I'll run through this tutorial: https://support.system76.com/articles/enable-hibernation/

Debounce Keyboard Presses
--------------------------

The keyboard on this laptop seems to have a small problem where a key is sometimes registered as being pressed twice when I only pressed it once.
This is fairly uncommon, but it's happening a lot more than my last laptop's keyboard.
The solution to this in Pop!_OS is to go to Settings -> Accessibility -> Typing -> Typing Assist (AccessX) -> Bounce Keys.
Now set the "Acceptance delay" to be very, very small. I mean small as in almost all the way to the left. If you make it even slightly too long,
it will not really be a debounce and is more designed for people who actually need accessibility for this kind of thing.
For fun, I'll enable "Beep when a key is rejected" because it means that, in theory, I should hear when one of my keypresses is rejected.
Sure enough, just 2 minutes into some coding, I hear a "ding" after finishing a word.
I didn't mean to input that character twice, but I guess my physical keyboard thought I typed that character twice.
Ha! Not today keyboard. I have software to fix you!

To see what value was set here, you can run ``gsettings get org.gnome.desktop.a11y.keyboard bouncekeys-delay``
A value of 55 seems to work decently.
See also: https://unix.stackexchange.com/a/530090

A better debounce (Update November 7)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above keyboard bounce is OK... Actually no, it's pretty bad.
I found `this stack exchange answer <https://unix.stackexchange.com/a/593086/591317>`_.

.. code-block::

  apt install xkbset
  xkbset bo 50
  xkbset exp =bo

After some testing, it's pretty much the exact same as the first solution, so it's not really better, just another option.

I might try this later: https://github.com/finkrer/KeyboardChatteringFix-Linux


New SSD
-----------

https://manpages.ubuntu.com/manpages/lunar/en/man8/mount.ntfs.8.html

I got a Samsung SSD installed in my M.2 spot.
I partitioned it with a GPT partition table.
I need to create an ``/etc/fstab`` entry for it.
I use ``ls -l /dev/disk/by-uuid/`` to get the UUID for my drive, which is mounted at ``/dev/nvme1n1p1``.
The ID is ``23D17A16325AFC50``, so my entry will look like this:

.. code-block::

  UUID=23D17A16325AFC50 /srv/extreme ntfs-3g windows_names,hide_dot_files,norecover,uid=0,gid=2505,umask=003 0 0

Reasons for each option:

* ``windows_names`` - prevent Linux from creating files with names not compatible with Windows
* ``hide_dot_files`` - when Linux creates a file or directory beginning with ``.``, it should appear hidden on Windows
* ``norecover`` - If Windows did not unmount this drive properly, then we don't need to try and mount it
* ``uid=0`` and ``gid=2505`` - All files should appear with ownership root:extreme, where extreme is the group I create below
* ``umask=003`` - keep read permission for others, but take away write and execute permissions


Creating the ``extreme`` group:

.. code-block:: shell

  sudo groupadd --gid 2505 extreme
  sudo usermod --append --groups extreme lavender

ACPI Error Crashes Pop!_OS When Awake from Suspend after plugging in external monitor
----------------------------------------------------------------------------------------

So yeah, sometimes when I plug my external monitor in right before awaking from suspend, I get some errors.
Sometimes not even if I plug in an external monitor.
Here's a snippet of ``journalctl``.

.. code-block::

  Oct 23 15:01:39 lavender-legion kernel: Freezing user space processes
  Oct 23 15:01:39 lavender-legion kernel: Freezing user space processes completed (elapsed 0.002 seconds)
  Oct 23 15:01:39 lavender-legion kernel: OOM killer disabled.
  Oct 23 15:01:39 lavender-legion kernel: Freezing remaining freezable tasks
  Oct 23 15:01:39 lavender-legion kernel: Freezing remaining freezable tasks completed (elapsed 0.001 seconds)
  Oct 23 15:01:39 lavender-legion kernel: printk: Suspending console(s) (use no_console_suspend to debug)
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: interrupt blocked
  Oct 23 15:01:39 lavender-legion kernel: ACPI: PM: Preparing to enter system sleep state S3
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: event blocked
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: EC stopped
  Oct 23 15:01:39 lavender-legion kernel: ACPI: PM: Saving platform NVS memory
  Oct 23 15:01:39 lavender-legion kernel: Disabling non-boot CPUs ...
  Oct 23 15:01:39 lavender-legion kernel: smpboot: CPU 1 is now offline
  ...
  Oct 23 15:01:39 lavender-legion kernel: smpboot: CPU 23 is now offline
  Oct 23 15:01:39 lavender-legion kernel: ACPI: PM: Low-level resume complete
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: EC started
  Oct 23 15:01:39 lavender-legion kernel: ACPI: PM: Restoring platform NVS memory
  Oct 23 15:01:39 lavender-legion kernel: Enabling non-boot CPUs ...
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 1 APIC 0x1
  Oct 23 15:01:39 lavender-legion kernel: CPU1 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 2 APIC 0x8
  Oct 23 15:01:39 lavender-legion kernel: CPU2 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 3 APIC 0x9
  Oct 23 15:01:39 lavender-legion kernel: CPU3 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 4 APIC 0x10
  ...
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 14 APIC 0x38
  Oct 23 15:01:39 lavender-legion kernel: CPU14 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 15 APIC 0x39
  Oct 23 15:01:39 lavender-legion kernel: CPU15 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 16 APIC 0x40
  Oct 23 15:01:39 lavender-legion kernel: core: cpu_atom PMU driver: PEBS-via-PT
  Oct 23 15:01:39 lavender-legion kernel: ... version:                5
  Oct 23 15:01:39 lavender-legion kernel: ... bit width:              48
  Oct 23 15:01:39 lavender-legion kernel: ... generic registers:      6
  Oct 23 15:01:39 lavender-legion kernel: ... value mask:             0000ffffffffffff
  Oct 23 15:01:39 lavender-legion kernel: ... max period:             00007fffffffffff
  Oct 23 15:01:39 lavender-legion kernel: ... fixed-purpose events:   3
  Oct 23 15:01:39 lavender-legion kernel: ... event mask:             000000070000003f
  Oct 23 15:01:39 lavender-legion kernel: CPU16 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 17 APIC 0x42
  Oct 23 15:01:39 lavender-legion kernel: CPU17 is up
  ...
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 22 APIC 0x4c
  Oct 23 15:01:39 lavender-legion kernel: CPU22 is up
  Oct 23 15:01:39 lavender-legion kernel: smpboot: Booting Node 0 Processor 23 APIC 0x4e
  Oct 23 15:01:39 lavender-legion kernel: CPU23 is up
  Oct 23 15:01:39 lavender-legion kernel: ACPI: PM: Waking up from system sleep state S3
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: interrupt unblocked
  Oct 23 15:01:39 lavender-legion kernel: ACPI: EC: event unblocked
  Oct 23 15:01:39 lavender-legion kernel: nvme nvme1: Shutdown timeout set to 8 seconds
  Oct 23 15:01:39 lavender-legion kernel: nvme nvme1: 24/0/0 default/read/poll queues
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: No handler for Region [RTCM] (00000000e3b61ac4) [SystemCMOS] (20230331/evregion-130)
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Region SystemCMOS (ID=5) has no handler (20230331/exfldio-261)
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: No Local Variables are initialized for Method [SNTM]
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: No Arguments are initialized for method [SNTM]
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Aborting method \_SB.PC00.LPCB.EC0.SNTM due to previous error (AE_NOT_EXIST) (20230331/psparse-529)
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Aborting method \_SB.PC00.LPCB.EC0._Q77 due to previous error (AE_NOT_EXIST) (20230331/psparse-529)
  Oct 23 15:01:39 lavender-legion kernel: nvme nvme0: 24/0/0 default/read/poll queues
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: No handler for Region [RTCM] (00000000e3b61ac4) [SystemCMOS] (20230331/evregion-130)
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Region SystemCMOS (ID=5) has no handler (20230331/exfldio-261)
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: No Local Variables are initialized for Method [SNTM]
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: No Arguments are initialized for method [SNTM]
  Oct 23 15:01:39 lavender-legion kernel:
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Aborting method \_SB.PC00.LPCB.EC0.SNTM due to previous error (AE_NOT_EXIST) (20230331/psparse-529)
  Oct 23 15:01:39 lavender-legion kernel: ACPI Error: Aborting method \_SB.PC00.LPCB.EC0._Q77 due to previous error (AE_NOT_EXIST) (20230331/psparse-529)
  Oct 23 15:01:39 lavender-legion kernel: usb 1-11: reset high-speed USB device number 5 using xhci_hcd
  Oct 23 15:01:39 lavender-legion kernel: pcieport 0000:00:1d.4: PCI bridge to [bus 0e]
  Oct 23 15:01:39 lavender-legion kernel: pcieport 0000:00:1d.4:   bridge window [mem 0x83100000-0x831fffff]
  Oct 23 15:01:39 lavender-legion kernel: pcieport 0000:00:1b.5: PCI bridge to [bus 08]
  Oct 23 15:01:39 lavender-legion kernel: pcieport 0000:00:1b.5:   bridge window [io  0x4000-0x4fff]
  Oct 23 15:01:39 lavender-legion kernel: pcieport 0000:00:1b.5:   bridge window [mem 0x83200000-0x832fffff]
  Oct 23 15:01:39 lavender-legion kernel: OOM killer enabled.
  Oct 23 15:01:39 lavender-legion systemd-resolved[1122]: Clock change detected. Flushing caches.
  Oct 23 15:01:39 lavender-legion acpid[1188]: client 3379[1000:1000] has disconnected
  Oct 23 15:01:39 lavender-legion systemd-logind[1229]: Lid opened.
  Oct 23 15:01:39 lavender-legion systemd[1]: Starting Refresh fwupd metadata and update motd...
  Oct 23 15:01:39 lavender-legion kernel: Restarting tasks ... done.
  Oct 23 15:01:39 lavender-legion kernel: random: crng reseeded on system resumption
  Oct 23 15:01:39 lavender-legion kernel: thermal thermal_zone11: failed to read out thermal zone (-61)
  Oct 23 15:01:39 lavender-legion systemd[1]: fwupd-refresh.service: Deactivated successfully.
  Oct 23 15:01:39 lavender-legion systemd[1]: Finished Refresh fwupd metadata and update motd.
  ...

With some of that output, I was able to find this answer: https://unix.stackexchange.com/a/593539.
The answer recommends adding ``acpi=off`` via the grub menu.
Problem is, I don't actually have grub installed yet.
It might be worth installing the grub bootloader to potentially fix this annoying problem.

It turns out that Pop!_OS `uses Systemd-boot by default <https://support.system76.com/articles/bootloader/>`_.
A quick run of ``[ -d /sys/firmware/efi ] && echo "Installed in UEFI mode" || echo "Installed in Legacy mode"`` shows that I am in UEFI mode.
I won't continue with the tutorial because it's about repairing the bootloader, rather than changing it.

To understand Systemd-boot a little better, you can read: https://wiki.archlinux.org/title/Systemd-boot.
A quick run of ``sudo bootctl list`` shows all the OSes it knows about.
It seems to be correct.
A quick search of "pop!_os set kernel parameters" brings up many good links for setting kernel parameters in Pop!_OS.
Running ``sudo kernelstub --print-config`` shows that my kernel boot options are ``quiet loglevel=0 systemd.show_status=false splash``.
Now I run ``sudo kernelstub --add-options "acpi=off"`` and confirm that the options now contain ``acpi=off``.

After some more research, this Q and A (https://access.redhat.com/solutions/58790) makes me think that
ACPI is pretty much necessary for a laptop to be functional as a laptop with suspend functionality.
I think I won't try to boot with ACPI disabled.

Configuring Screen Lock and Blank Delays
-------------------------------------------

Since NVIDIA drivers are weird, I made these changes:

* Power

  * Screen Blank: Never
  * Automatic Suspend

    * Plugged in: Delay: 2 hours

I couldn't figure out how to stop the screen from going blank right after locking the computer, though.

Middle click lower window
--------------------------

With gnome tweaks installed, go to Window Titlebars > Titlebar Actions > Middle-Click: Lower.

Because of this, I prefer to have things like Firefox and IntelliJ have the system title bar.
On Firefox, right click on title bar, then select "Customize Toolbar". In the bottom left, select "Title Bar".

For IntelliJ: Appearance & Behavior > Appearance > UI Options > "Merge main menu with window title": Uncheck this

September 14, 2024 - alacritty in nautilus
----------------------------------------------

Adding this here because I don't feel like creating another page

https://askubuntu.com/a/1275458

.. code-block:: shell

  sudo update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /home/lavender/.local/bin/alacritty 50
  sudo update-alternatives --config x-terminal-emulator

Note that this doesn't work at the time of writing. It might just not work...
I'll report back eventually. Maybe I'll delete this section.

I also gave this a try: https://github.com/Stunkymonkey/nautilus-open-any-terminal

.. code-block:: shell

  sudo apt-get install -y python3-pip
  pip install --user nautilus-open-any-terminal
  glib-compile-schemas ~/.local/share/glib-2.0/schemas/

I could not get either of those to work.
Not sure why. That's a problem for later.
