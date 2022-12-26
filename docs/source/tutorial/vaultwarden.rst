Vaultwarden
============

This tutorial will show how to set up https://hub.docker.com/r/vaultwarden/server


.. code-block:: shell

  cd /opt/containers
  mkdir vaultwarden && cd vaultwarden
  mkdir data/
  # In this case, we will keep the owner of data/ to be 0:0

Now we can edit ``docker-compose.yml``

.. code-block:: yaml

  version: '3'
  services:
    vaultwarden:
      image: vaultwarden/server:latest
      container_name: vaultwarden
      volumes:
        - ./data:/data
      environment:
        SIGNUPS_ALLOWED: "false"
        INVITATIONS_ALLOWED: "true"
        #SIGNUPS_DOMAINS_WHITELIST: "gmail.com,outlook.com"
      restart: unless-stopped
  networks:
    default:
      name: $DOCKER_MY_NETWORK


.. note:: 

  If you put this behind a reverse proxy such as Caddy, you cannot use basic auth because Caddy will pass the username and password
  to vaultwarden, which will make the session expire immediately upon login.

Using Vaultwarden
------------------

Once you are signed up, you can set ``SIGNUPS_ALLOWED`` to "false". You can also create an organization so that you can invite others.
You can use the Bitwarden app on your phone to acess your data, or you can use the Vaultwarden web interface.
