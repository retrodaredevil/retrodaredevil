OpenTTD
========

OpenTTD is a fun and free game: https://www.openttd.org/

You should generate a ``.sav`` file locally using the OpenTTD client.

.. code-block:: shell

    cd /opt/containers/
    # Replace MyGame with something of your choosing. The name of this does not matter, but it will be the name of your docker container
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


