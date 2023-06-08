Graylog
==========

Graylog in Docker
------------------

I have a (somewhat outdated at the time of writing) tutorial for this here:
https://solarthing.readthedocs.io/en/latest/logging.html#setting-up-graylog

Graylog in Linux Container
---------------------------

Graylog running in docker is possible, but if you have Proxmox setup, you can also instead just install Graylog in LXC!

I recommend creating a Debian 11 LXC.
You can name it whatever you would like, but I asked ChatGPT "What type of fish is good at remembering and logging things that happen?"
and it told me that archerfish are good at recalling visual characterists of their prey, so I'll make ``archerfish`` my hostname.
Here's my final options:

.. figure:: ../../images/2023-06-06-graylog-proxmox-lxc-container-create-confirm.png
  :width: 500px

Now get into your container and start following the tutorial here: https://go2docs.graylog.org/5-1/downloading_and_installing_graylog/debian_installation.htm

.. code-block:: shell

  apt-get update
  apt-get install -y gnupg curl
  # Note that apt-key is apparently deprecated. TODO update this with an alternative
  wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
  echo "deb http://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
  apt-get update
  apt-get install -y mongodb-org

  systemctl daemon-reload
  systemctl enable mongod.service
  systemctl restart mongod.service
  systemctl --type=service --state=active | grep mongod

Historically Graylog has used Elastisearch, but we're going to install OpenSearch.

.. code-block:: shell

  curl -o- https://artifacts.opensearch.org/publickeys/opensearch.pgp | apt-key add -
  echo "deb https://artifacts.opensearch.org/releases/bundle/opensearch/2.x/apt stable main" | tee -a /etc/apt/sources.list.d/opensearch-2.x.list
  apt-get update
  # if you would like to, at this point you may run `apt list -a opensearch` and use `apt-get install opensearch=2.5.0` to install a specific version
  # At the time of writing 2.8.0 is the latest and is the one I want to install, so I won't specify the version explicitly
  apt-get install opensearch

Now we must configure opensearch.
Edit ``/etc/opensearch/opensearch.yml`` and make sure the fields below are updated (don't delete any other lines).

.. code-block::

  cluster.name: graylog
  node.name: ${HOSTNAME}
  path.data: /var/lib/opensearch
  path.logs: /var/log/opensearch
  discovery.type: single-node
  network.host: 0.0.0.0
  action.auto_create_index: false
  plugins.security.disabled: true

Edit ``/etc/opensearch/jvm.options``.
Update ``-Xms1g`` and ``-Xmx1g`` to be half of your system ram.
``-Xms2g`` and ``-Xmx2g`` in the case of my container.

Now, on your Proxmox host, run these commands:

.. code-block::

  sysctl -w vm.max_map_count=262144
  echo 'vm.max_map_count=262144' >> /etc/sysctl.conf

Now in your container:

.. code-block:: shell

  systemctl daemon-reload
  systemctl enable opensearch.service
  systemctl start opensearch.service

Since we have installed OpenSearch, we can now get into installing Graylog.

.. code-block:: shell

  wget https://packages.graylog2.org/repo/packages/graylog-5.1-repository_latest.deb
  dpkg -i graylog-5.1-repository_latest.deb
  apt-get update 
  apt-get install -y graylog-server
  rm 'graylog-5.1-repository_latest.deb'

Before starting graylog we need to edit the configuration file.
We will edit ``/etc/graylog/server/server.conf``.

* Set ``root_password_sha2`` to the output of ``(read -s PASS && printf $PASS | sha256sum)`` (after you type your password).
* Set ``password_secret`` to the output of ``< /dev/urandom tr -dc A-Z-a-z-0-9 | head -c${1:-96};echo;``
* Set ``http_bind_address=0.0.0.0:9000`` (might not be the most secure thing, but it's easy).

Now save and run these commands to start it:

.. code-block:: shell

  systemctl daemon-reload
  systemctl enable graylog-server
  systemctl start graylog-server

Yay! It's setup now! I recommend you make this container a template.
Make a full clone, start it up, then access it at ``http://IP:9000``.
You can see what your container's IP address is with ``ip addr``.
Login with admin/yourpassword.

