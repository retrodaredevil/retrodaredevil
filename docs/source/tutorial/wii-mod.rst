Modding Nintendo Wii
=======================

Modding your Wii is easy! This page aims to point to other links so that you (or my future self) can figure this out more easily.

The link to start is: https://wii.guide/

For my install, I did all of the setup using an SD card, then I use my USB hard drive exclusively for games, 
as I don't believe the homebrew channel allows loading apps from NTFS formatted drives.

Tools used
-----------

Much of this stuff you don't need anything installed for (as long as you can do basic extract or reformat SD card).
But, if you want to convert a ``.iso`` to a ``.wbfs``, you can use something like https://wit.wiimm.de/.
Download wit's tar archive and install it using ``./install.sh``.
To check that it is working, you can do something like ``wit LLLL nameoffile.iso`` to view info about an iso file.

Note that Wii Backup Manager is a more popular and user friendly choice for Windows users.

Playing Games on SD Card or USB Drive
------------------------------------------

https://wii.guide/wiiflow

You will want to format your SD card or USB drive to FAT32 or NTFS. YOU SHOULD USE NTFS as FAT32 will not support larger games.
However, I believe that SD cards may not work with NTFS.
This instructions are pretty much the same for both SD card and USB drives, so you can always copy files from one to the other.
On Linux I use GParted to reformat drives.

You put games in a location such as ``/wbfs/Name of Game/game-asdf [GAMEID].wbfs``.
The GAMEID can be found at https://www.gametdb.com/. Sometimes, depending on the file name of the wbfs file, 
it will work without that specific format, but I don't know exactly what the criteria for the filename is, so I usually stick with what works.
For instance, Mario Party 8 can be in a location such as ``/wbfs/Mario Party 8 [RM8E01].wbfs`` (or it can be placed in its own directory with that same filename).

Game Specifics
---------------

Guitar Hero 5
^^^^^^^^^^^^^^

Launching Guitar Hero 5 via WiiFlow requires IOS222 or IOS223.

* https://gbatemp.net/threads/loading-guitar-hero-5-and-band-hero-error.198404/
* https://wiibrew.org/wiki/IOS222

