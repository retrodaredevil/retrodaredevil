Docker
=========

Docker is an awesome way to containerize your applications to make them easier to backup and manage.

.. note:: 

  This page is incomplete. I plan to add more documentation to it later.


Docker Compose
----------------

Many tutorials in this documentation will use ``docker-compose.yml`` files.

Useful Commands
-----------------

.. _docker_compose_attach:

Attach to a compose file's container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, make sure that ``jq`` is installed: ``sudo apt-get install -y jq``.
Then, copy this code into a file called ``compose-attach`` somewhere in your ``$PATH`` and make it executable.

.. code-block:: shell

  #!/usr/bin/env bash
  argument="$1"
  if [ ! -n "$argument" ]; then
    # argument is empty
    container_id=$(sudo docker compose ps --format json | jq -r '.[0] | .ID')
  else
    container_id=$(sudo docker compose ps --format json | jq -r ".[] | select(.Name | test(\"^$argument\$\")) | .ID")
  fi
  if [ ! -n "$container_id" ]; then
    echo "Invalid container!"
    exit 1
  fi
  sudo docker attach "$container_id"


To detach, press CTRL+P, CTRL+Q.

Docker Networking
---------------------------

Docker Compose Links
^^^^^^^^^^^^^^^^^^^^^

We know that docker's `--link feature <https://docs.docker.com/network/links/>`_ is deprecated.
However, docker compose has a links feature that is a bit different.
The `docs for compose links <https://docs.docker.com/compose/networking/#link-containers>`_ (and `services links <https://docs.docker.com/compose/compose-file/05-services/#links>`_) do not have a note about them being legacy or deprecated.
However, here are a few URLs that have discussion about this feature being something you should not use:

* https://github.com/docker/docs/issues/4543

  * Links are not supported by ``docker stack deploy``.

* https://stackoverflow.com/a/41294598/5434860

  * "Links have been replaced by networks"

* https://serverfault.com/questions/833592/are-links-deprecated-in-docker-compose

  * Do discussion here, but it asks the exact question I was trying to answer.

More than 30 bridge networks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* https://stackoverflow.com/questions/51439074/docker-limit-user-defined-bridge-networks

  * Manually specify the subnet when creating the network
  * Change ``"default-address-pools"``: https://docs.docker.com/engine/reference/commandline/dockerd/#on-linux

* https://stackoverflow.com/questions/43720339/docker-error-could-not-find-an-available-non-overlapping-ipv4-address-pool-am
* https://github.com/moby/moby/pull/36396



