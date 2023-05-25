\*arr
=====

This page is incomplete, but has pieces of documentation for configuring the \*arrs.
This page utilizes many docker images provided by `linuxserver.io <https://www.linuxserver.io/>`_. Thanks linuxserver.io!

TODO

* Insert docker compose file
* Check out integration with :docker-hub:`linuxserver/calibre-web`, :docker-hub:`linuxserver/calibre` and :docker-hub:`linuxserver/lazylibrarian`.
* Document integration with the ReadEra app.

Radarr/Sonarr
---------------

This link can be a good starting point: https://trash-guides.info/Radarr.
Plus, if you eventually want to setup multiple instances of either Radarr or Sonarr, you can follow this part of the guide: https://trash-guides.info/Radarr/Tips/Sync-2-radarr-sonarr/.


Readarr
--------

The above docker compose file utilized the :docker-hub:`linuxserver/readarr` docker container.

.. note::

  Readarr does not support the downloading of both E-books and audiobooks for the same book.
  If you want this, you should complete this setup, then clone your readarr-config directory to have two identical instances.
  At that point you can configure each instance to download E-books and audiobooks, respectively.

Once you have launched Readarr, you will need to add a root folder.
Name it whatever you want and make the path ``/books`` (or whatever is referenced in your ``docker-compose.yml``).
Save that configuration. 

Download Clients
^^^^^^^^^^^^^^^^^

Now go to settings > download clients. 

Add a download client. Choose transmission.
Name: ``Transmission`` or whatever you want.
Host: ``transmission-openvpn``, or the host of the download client, which depends on its container name.
Port: ``9091`` (default). Rest use defaults.

Add a remote path mapping with: Host: ``transmission-openvpn``, or choose the same as above.
Remote path: ``/data/completed``, or the path inside your download client uses (determined by its docker compose configuration).
Local path: ``/downloads``, or the path defined in your docker compose for readarr inside its container.

Indexers
^^^^^^^^^

.. note::

  If you are using something other than Jackett for an API for your trackers, these instructions may be different.

Now go to Settings > Indexers. Add an indexer. Choose "Torznab".
Set the URL to the torznab for the given tracker in Jackett by clicking "Copy Tornzab Feed" in Jackett. 
After copying, replace the first part of the URL with ``http://jackett:9117``, or the hostname of your jackett container.
Set the API Key to Jackett's API key.
Use the Categories provided already, and optionally add "Audio/Audiobook", "Books", "Audio Books", "E-books", "Comics".
Make if the test is not successful, it may be because of the URL, or incorrect categories.


