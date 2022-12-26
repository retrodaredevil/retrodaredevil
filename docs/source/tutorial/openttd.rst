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
* Terrain type: "Very Flat" - we don't like terrain that is super hilly
* Make all the map edges water

Settings (these can be changed in ``openttd.cfg`` later)
  
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

Sending Console Commands
---------------------------

You can see a list of console commands here: https://bookstack.jeroen-eland.nl/books/knowledge-base/page/openttd-console-commands.
The subsections below show how to send console commands.

Attaching to the docker container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To attach to the container and send commands, first run ``docker ps`` and get the ``CONTAINER ID`` of the running container.
Once you have that ID, run ``docker attach <CONTAINER ID>``.
You can see more about attaching here: :ref:`docker_compose_attach`.

Admin port
^^^^^^^^^^^

You can connect to the admin port to send console commands. I have no idea how to do this, so here's the doc: https://wiki.openttd.org/en/Development/Server%20admin%20port.


Edit settings in ``openttd.cfg``
----------------------------------

Changes to ``openttd.cfg`` can be made by either directly editing the file itself, or by using console commands.

https://wiki.openttd.org/en/Archive/Manual/Settings/Openttd.cfg

.. code-block::

  set network.client_name God
  set network.server_name TrainLand
  set network.min_active_clients 1
  list_settings
  list_cmds

  # https://wiki.openttd.org/en/Manual/Dedicated%20server#controlling-the-server-with-rcon
  set network.rcon_passwordd asdf
  rcon_pw asdf

Other commands
---------------


* List commands: ``list_cmds``
* Get IDs of all companies: ``players`` or ``companies``.
* Remove company: ``reset_company <company ID>``


