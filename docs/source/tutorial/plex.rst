Plex
=====

Running Plex gives you an awesome media experience!
This documents its ``docker-compose.yml`` file and additional add-ons.


.. code-block:: yaml

  version: '3'
  services:
    plex:
      container_name: plex
      image: plexinc/pms-docker
      restart: unless-stopped
      environment:
        - TZ=US/Chicago
        - PLEX_CLAIM=claim-YOURSECRETCLAIM
      network_mode: host
      volumes:
        - ./config:/config
        - ./transcode:/transcode
        - /srv/location1/media/public:/data:ro
      devices:
        # Allows for hardware transcoding
        - "/dev/dri:/dev/dri"

Additions
-----------

Here are some cool programs you can use to supplement your Plex installation:

* `Plex Meta Manager <https://metamanager.wiki/en/latest/>`_ - automatically create cool collections
* `Tautulli <https://tautulli.com/>`_ - view cool statistics about your server. (Becomes irrelevant if you use Plex Dash: https://www.plex.tv/plex-labs/)
* `Varken <https://github.com/Boerderij/Varken>`_ - send Plex statistics to InfluxDB for viewing on a Grafana frontend
* `Servarr <https://wiki.servarr.com/>`_ has good documentation for things to use alongside Plex
* Here's a GitHub with many docker compose files: https://github.com/vaeyo/MediaServer-DockerComposeFiles

Transcoding
--------------

Hardware Transcoding in Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To enable hardware transcoding for a Docker install of plex, you must add ``/dev/dri`` as a device.
You should not do this if you have an integrated graphics as I have found Plex thinks it's hardware transcoding,
but is actually worse than if HW transcoding was disabled.

You can run this command to see infomration about your GPU:

.. code-block:: shell

  # Credit to https://askubuntu.com/a/392944/756467
  lspci | grep ' VGA ' | cut -d" " -f 1 | xargs -i lspci -v -s {}

Subtitles and Transcoding
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes using subtitles will require Plex to transcode to burn-in the subtitles. More info here:
https://support.plex.tv/articles/200471133-adding-local-subtitles-to-your-media/
