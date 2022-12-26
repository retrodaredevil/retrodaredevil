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

Attach to a compose file's container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

  sudo apt-get install -y jq
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
