Minecraft Server
=====================

Minecraft is awesome!!!

This tutorial shows how to configure a docker container to run a Minecraft server.

Server Jar Generation
----------------------

You can use any server jar you would like. I like to use Spigot. You can follow their tutorial here: https://www.spigotmc.org/wiki/buildtools/

You will likely need a particular version of Java. I recommend installing SDKMAN: https://sdkman.io/install.
SDKMAN is easy to install for your local user, so I recommend building the jar file as your local user, rather than with sudo.

.. note:: 

  Running buildtools may alter your ``.gitconfig`` file. More information here: https://www.spigotmc.org/threads/buildtools-jar-messes-with-local-gitconfig.37433/


Server Setup
-------------

.. code-block:: shell

  cd /opt/containers
  mkdir minecraft
  cd minecraft
  # Replace MyGame with a name of your choosing
  mkdir jars/ MyGame/
  # Place your server jar file in the jars folder
  cd MyGame/
  mkdir data config
  chown 1000:1000 data config

.. note::

  The ``itzg/minecraft-server`` docker image does support different UID and GID, 
  which can be set by environment variables in the below configuration.

.. note:: 
  
  The below configuration implicitly uses the ``latest`` tag, which uses one of the most recent JDKs.
  Older Minecraft server versions are incompatible with new JDKs/JREs (Version of Java).
  You may have to choose a different tag for an older server version here: https://hub.docker.com/r/itzg/minecraft-server/tags

.. code-block:: yaml

  version: '3'
  # https://github.com/itzg/docker-minecraft-server/blob/master/README.md#using-docker-compose
  services:
    minecraft-server:
      container_name: minecraft-MyGame
      image: itzg/minecraft-server
      restart: unless-stopped
      environment:
        - TZ=US/Chicago
        - TYPE=CUSTOM
        - CUSTOM_SERVER=/jars/spigot-1.17.1.jar
        - EULA=TRUE
        - EXEC_DIRECTLY=true
      volumes:
        - ./data:/data
        - ./config/bukkit.yml:/data/bukkit.yml
        - ./config/commands.yml:/data/commands.yml
        - ./config/help.yml:/data/help.yml:ro
        - ./config/server.properties:/data/server.properties:ro
        - ./config/spigot.yml:/data/spigot.yml
        - ../jars:/jars:ro
      ports:
        - "25565:25565"
      tty: true
      stdin_open: true

