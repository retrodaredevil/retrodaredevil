OpenRCT2 Server
=================

OpenRCT2 is a game about creating amusement parks. More info here: https://openrct2.org/.
Issue page: https://github.com/OpenRCT2/OpenRCT2/issues?q=is%3Aissue+is%3Aopen+-author%3AOpenRCT2-git-bot+

This tutorial will show how to set up an OpenRCT2 server based on this docker image: https://github.com/OpenRCT2/openrct2-docker (https://hub.docker.com/r/openrct2/openrct2-cli)

Useful links:

* https://docs.openrct2.io/en/latest/index.html
* https://github.com/OpenRCT2/OpenRCT2/wiki/Multiplayer#setting-permissions

Client Setup
--------------

Before you setup your server, get your client up and running.
On Linux you can use flatpak: (https://flathub.org/apps/details/io.openrct2.OpenRCT2, https://github.com/OpenRCT2/OpenRCT2/wiki/Getting-packaged-versions#flatpak)

.. code-block:: shell

  flatpak install flathub io.openrct2.OpenRCT2
  flatpak run io.openrct2.OpenRCT2

When running it will ask whether you have the game installed or have the installer, tell it that you have the installer.
Select the ``.exe`` file on your system that you bought from a trusted source like Steam or something.

Use the client to create a save file that we will use later.
For a Flatpak install, the save file is located in ``~/.var/app/io.openrct2.OpenRCT2/config/OpenRCT2/save/autosave/``.

Server Setup
---------------

The first thing that is worth mentioning is that the server and client are effectively identical (just like openttd).
The cool thing about this is how powerful the command line interface is.
In fact, that's all the docker container is. It's effectively the same as calling ``flatpak run io.openrct2.OpenRCT2 ... --headless``.
Since we will make the server run headless, the server does not need the assets from RCT1 or RCT2.

.. code-block:: shell

  cd /opt/containers
  mkdir -p openrct2/MyGame
  cd openrct2/MyGame
  mkdir -p openrct2-game/save/autosave

  mv YOUR_SAVE_FILE.sv6 openrct2-game/save/autosave/

  chown 2000:2000 -R openrct2-game

  git clone https://github.com/retrodaredevil/openrct2-docker


Now you can edit ``docker-compose.yml``

.. code-block:: yaml

  version: "3.7"
  services:
    openrct2-MyGame:
      container_name: openrct2-MyGame
      restart: "no"
      user: 2000:2000
      build:
        context: ./openrct2-docker/0.4.3/cli
        dockerfile: Dockerfile
      ports:
        # OpenRCT2 only uses TCP
        - "11753:11753/tcp"
      volumes:
        - ./openrct2-game:/app/game

Now we have our compose file complete. When the game is first run,
the startup script will choose the only available save file and lots of files will be populated into ``openrct2-game``.
In my experience the first time this is run, the server will keep running and try to advertise itself, but will not be able to be connected to.
That's OK. Stop the container with ``sudo docker compose stop``.
We need to edit the ``config.ini`` file.

The ``config.ini`` file
-------------------------

Let's edit the ``config.ini`` file, which is located in ``openrct2-game/config.ini``.

* Set ``sound.sound`` to ``false``.
* Set ``network.advertise`` to ``false``.
* Set ``network.player_name`` to ``"God"``.
* Set ``network.known_keys_only`` to ``true``. Note: Consider only enabling this after authorizing the client.
* Set ``network.pause_server_if_no_clients`` to ``true``.
* Change ``network.server_name``, ``network.default_password`` if desired.

Authorizing Clients
--------------------

Use this to give a player admin: https://github.com/OpenRCT2/OpenRCT2/wiki/Multiplayer-permissions (https://github.com/OpenRCT2/OpenRCT2/pull/3699)
This will also make them "known".
Look in the ``.var/app/io.openrct2.OpenRCT2/config/OpenRCT2/keys/`` (flatpak install location). The name of the file of your public key is the SHA1.
Make yourself an admin by editing ``openrct2-game/users.json`` and making an entry for your users with the 
same structure as the "God" user.
Once you are an Admin, move other players to the "User" group. Once added to the user group, their SHA1 key will be automatically populated in ``users.json``.

