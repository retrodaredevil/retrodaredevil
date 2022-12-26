OpenTTD Server
================

OpenTTD is a fun and free game: https://www.openttd.org/
This tutorial shows how to set up a server for multiplayer.

Screenshots: https://www.openttd.org/screenshots

.. figure:: https://www.openttd.org/screenshots/1.9-darkuk-2.png
  :width: 500px

Save file creation
-------------------

Create the save file using the client.
When creating the save file, I recommend changing some of the defaults. Some of these settings cannot be changed later.

* Choose a climate: https://wiki.openttd.org/en/Manual/Climates
* Add mod "New GRF" - "Some vehicles never expire"
* Terrain type: "Very Flat" - we don't like 
* Make all the map edges water


Server Setup
--------------

You should generate a ``.sav`` file locally using the OpenTTD client.

.. code-block:: shell

  cd /opt/containers/
  # Replace "MyGame" with something of your choosing here and in the configuration below
  mkdir -p openttd/MyGame
  cd openttd/MyGame
  mkdir -p openttd/save/autosave/
  mv YOUR_SAVE_FILE.sav openttd/save/autosave/
  chown -R 2000:2000 openttd

Now you are ready to edit ``docker-compose.yml``. Put these contents in that file.

.. code-block:: yaml

  version: "3.7"
  services:
    openttd-MyGame:
      image: bateau/openttd:12.2
      container_name: openttd-MyGame
      restart: unless-stopped
      ports:
        - "3979:3979/udp"
        - "3979:3979/tcp"
      environment:
        - "loadgame=last-autosave"
        - "PUID=2000"
        - "PGID=2000"
      volumes:
        - ./openttd:/home/openttd/.openttd
      tty: true
      stdin_open: true

Now you can start the server using ``docker compose up -d``.
It should be easy to connect to the server, but allowing players to do anything can be difficult.
I found that you must attach to the running container to issue commands to set the RCON password so players can execute commands to pause the game.
(This is why we have ``tty: true`` and ``stdin_open: true``).

To attach to the container and send commands, first run ``docker ps`` and get the ``CONTAINER ID`` of the running container.
Once you have that ID, run ``docker attach <CONTAINER ID>``.


Edit ``openttd.cfg``
----------------------

Recommended changes to make

Settings
  
* When paused allow: "all actions"
* Airports never expire: on
* Vehicles never expire: on
* Vehicle breakdowns: none
* Number of plane crashes: reduced
* Environment > Authorities

  * Town council's attitude towards area restructuring: Permissive
  * Towns are allowed to build grade crossings: Off

* Town cargo generation: Quadratic
* Flat area around industries: 4 tiles

Direct changes to make

* Edit ``network.min_active_clients`` to 1 so that the game automatically pauses when no players are connected
