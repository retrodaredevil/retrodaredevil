Guacamole
==========

Guacamole is a remote desktop gateway. More info here: https://guacamole.incubator.apache.org/

This tutorial will be based off of https://github.com/boschkundendienst/guacamole-docker-compose.
This will utilize :docker-hub:`guacamole/guacamole`, :docker-hub:`guacamole/guacd` and :docker-hub:`_/postgres`.

.. note::

  If you don't like this tutorial, check out this one: https://blog.gurucomputing.com.au/remote-administration-with-guacamole/1-installing-guacamole/

.. code-block:: shell

  cd /opt/containers
  mkdir gaucamole
  cd guacamole
  mkdir init/
  chown 0:0 init/ # postgres does not care about the owner:group for this particular directory
  mkdir db/
  chown 2000:2000 db/
  # let drive/ and record/ directories be created by guacd

  docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > ./init/initdb.sql
  echo "POSTGRES_DATABASE=guacamole_db" >> .env
  echo "POSTGRES_USER=gauamole_user" >> .env
  echo "POSTGRES_PASSWORD=$(pwgen -N 1 -s 96)" >> .env


.. code-block:: yaml

  version: "3"

  services:
    guacd:
      image: guacamole/guacd
      restart: unless-stopped
      volumes: 
        - ./drive:/drive
        - ./record:/record
    postgres:
      image: postgres:15.1-bullseye
      user: 2000:2000
      environment:
        # Guacamole does not support a more modern authentication mechanism: https://issues.apache.org/jira/browse/GUACAMOLE-1608
        POSTGRES_HOST_AUTH_METHOD: password
        POSTGRES_DB: $POSTGRES_DATABASE
        POSTGRES_PASSWORD: $POSTGRES_PASSWORD
        POSTGRES_USER: $POSTGRES_USER

      restart: unless-stopped
      volumes:
        # Here's what the :z and :Z modes mean: https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label
        # Scripts inside /docker-entrypoint-initdb.d are only run if the data directory is empty
        - ./init:/docker-entrypoint-initdb.d:z
        - ./db:/var/lib/postgresql/data

    guacamole:
      # The official documentation recommends using container links (https://docs.docker.com/network/links/), 
      #   but compose will handle creating our own network, which effectively makes using links unnecessary
      container_name: guacamole
      image: guacamole/guacamole
      depends_on:
        - guacd
        - postgres
      environment:
        GUACD_HOSTNAME: guacd
        POSTGRES_HOSTNAME: postgres  # the name of the compose entry
        POSTGRES_DATABASE: $POSTGRES_DATABASE
        POSTGRES_PASSWORD: $POSTGRES_PASSWORD
        POSTGRES_USER: $POSTGRES_USER
  #    ports: # Uncomment these lines if you are not using a reverse proxy and want to directly expose an HTTP endpoint
  #      - 8080:8080/tcp
      restart: unless-stopped


  # Optionally include this if you specify the DOCKER_MY_NETWORK inside of your .env file
  networks:
    default:
      name: $DOCKER_MY_NETWORK


Now that you have ``docker-compose.yml`` complete, you can start the containers with ``docker compose up -d``.

.. note:: 

  This particular tutorial assumes that you can figure out how to access guacamole:8080 over a reverse proxy or directly.

Configuring Guacamole
-----------------------

Now that you have guacamole up and running, navigate to the web page in your browser.
Note that the path must be ``http(s)://myurl.myurl/guacamole``. (Append ``/guacamole`` to the end of your url).
To login, use ``guacadmin/guacadmin``. Navigate to settings > Preferences to change your password.

To connect to an RDP server, simply add a connection and connect to it.



Using Guacamole
----------------

After logging into a machine, it pretty much just works.
Copying and pasting text doesn't always work flawlessly, so be sure to check this out: https://guacamole.apache.org/doc/gug/using-guacamole.html#the-guacamole-menu.
Alternatively, go to ``about:config`` in Firefox and set ``dom.events.testing.asyncClipboard`` to true.
This allows the extraction of the clipboard, but not the pasting of clipboard content. This is not at all flawless.
