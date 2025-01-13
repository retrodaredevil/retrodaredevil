Commands
==========

Contains useful commands

Unix Commands
--------------

.. code-block::

  cat /etc/passwd | column -t -s ':' -N USERNAME,PW,UID,GUID,COMMENT,HOME,INTERPRETER -H PW

* ``column`` command - https://www.youtube.com/watch?v=uL7KvRskeog

  * Can even be given arguments to output JSON from CSV files

Public IP
-------------

Thanks https://www.tecmint.com/find-linux-server-public-ip-address/.
Script: https://github.com/retrodaredevil/common-util/blob/main/bin/public-ip

.. code-block:: shell

  dig +short myip.opendns.com @resolver1.opendns.com
  host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}'
  wget -qO- http://ipecho.net/plain | xargs echo
  wget -qO - icanhazip.com
  curl ifconfig.co
  curl ifconfig.me
  curl icanhazip.com

Find SSH Port
---------------

This example is for a ``192.168.1.0/24`` subnet.
Thanks https://serverfault.com/a/897620.

.. code-block:: shell

  nmap -p 22 --open -sV 192.168.1.0/24
