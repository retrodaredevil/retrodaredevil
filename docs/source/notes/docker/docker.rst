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
* https://straz.to/2021-09-08-docker-address-pools/

The default pool is given by this (https://github.com/moby/libnetwork/blob/67e0588f1ddfaf2faf4c8cae8b7ea2876434d91c/ipamutils/utils.go#L18-L21):

.. code-block:: json

  {
    "default-address-pools" : [
      {
        "base": "172.17.0.0/16",
        "size": 16
      },
      {
        "base": "172.18.0.0/16",
        "size": 16
      },
      {
        "base": "172.19.0.0/16",
        "size": 16
      },
      {
        "base": "172.20.0.0/14",
        "size": 16
      },
      {
        "base": "172.24.0.0/14",
        "size": 16
      },
      {
        "base": "172.28.0.0/14",
        "size": 16
      },
      {
        "base": "192.168.0.0/16",
        "size": 20
      }
    ]
  }

That means that we can create a total of :math:`3 * 2^{16-16} + 3 * 2^{16-14} + 1 * 2^{20-16} = 3 * 1 + 3 * 4 + 1 * 16 = 32` networks.
But we can't use the ``172.17.0.0/16`` network for bridge networks, so we are left with 31.
Remember that the ``"size"`` is the netmask of the individual networks, so by increasing it, we decrease the number of IP addresses allowed on a network, but increase the number of possible networks.
I'm going to change some of the 172.28.0.0/14, size:16 networks to be size 24.

With this change, I should be able to create many more networks without manually specifying the subnet for each of them.
Now I run ``sudo systemctl restart docker``.



