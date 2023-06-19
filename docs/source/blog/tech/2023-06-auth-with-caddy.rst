Authorization with Caddy (June 2023)
=======================================

I have been using Caddy for a while and I had been using Caddy's basic auth feature to protect each service that cannot be public.
The problem with basic auth is that I have to login to each service individually because my services are on different subdomains.
I had started looking into solutions to this, with a quick blob here: :ref:`authelia_research`.

June 17 - Setting up Authelia
---------------------------------

I finally got authelia working today (I had been playing with this for the past week and reading its docs).
I ran into a couple of problems, though.
The ``/config`` directory is being changed to have ``PUID`` and ``PGID`` ownership where those are defined environment variables.
This is a problem because I have been running authelia as the default (root:root) and I want to keep the contents of ``/config`` in version control.
I figured the easiest solution is changing PUID and PGID to 1000:1000, but that had the side effect of not allowing access to stuff in ``/run/secrets``.
ChatGPT suggested that I create a custom entrypoint.sh to change the permissions of the files in ``/run/secrets``, but I didn't like that.
It then suggested to add ``security_opt: - seccomp=unconfined - no-new-privileges``, but I didn't like the security risks that came with that.
I went on a search to figure out what part of the authelia code was changing my the ownership of ``/config``.
It turns out their entrypoint was `running chown <https://github.com/authelia/authelia/blob/ecf742aa33fbfa175ed27d7e5903a764febcb64d/entrypoint.sh#L10>`_.
Since the ``/config`` is hard coded, I figured if I changed the mount point to be ``/myconfig`` inside the container it wouldn't change the permissions.
Sure enough, the permissions remained unchanged. Perfect! Right?
Well, not exactly. For whatever reason this causes me to get an error in the authelia login page with:
``There was an issue retrieving global configuration`` with some error in the web console, but no error in the docker logs.
Frustrating.
So now what? Well, I took a closer look at the entrypoint.sh file and notice that maybe I can change the user without setting PUID and PGUID.
I could do it the native docker way! (Maybe I would still have access to secrets if I do it this way).
Let's try it. Nope. Still don't have access to the secrets.
Let's try to figure this out...
I found this thread! https://forums.docker.com/t/only-root-user-has-access-to-the-secret/102774.
Looks like there is a configuration I can add to my compose file to correctly set ownership of a secret. Let's try this:

.. code-block::

  # ...
      secrets:
        - source: AUTHELIA_JWT_SECRET
          target: /run/secrets/AUTHELIA_JWT_SECRET
          uid: "1000"
          gid: "1000"
          mode: 0440
        - source: AUTHELIA_SESSION_SECRET
          target: /run/secrets/AUTHELIA_SESSION_SECRET
          uid: "1000"
          gid: "1000"
          mode: 0440
        - source: AUTHELIA_STORAGE_ENCRYPTION_KEY
          target: /run/secrets/AUTHELIA_STORAGE_ENCRYPTION_KEY
          uid: "1000"
          gid: "1000"
          mode: 0440
        - source: POSTGRES_PASSWORD
          target: /run/secrets/POSTGRES_PASSWORD
          uid: "1000"
          gid: "1000"
          mode: 0440

Aaannd... It does not work. Went into the container to see if the permissions or ownership changed at all and they did not.
See:

.. code-block::

  /app # ls -l /run/secrets
  total 16
  -rw-------    1 root     root            65 Jun 17 21:52 AUTHELIA_JWT_SECRET
  -rw-------    1 root     root            65 Jun 17 21:52 AUTHELIA_SESSION_SECRET
  -rw-------    1 root     root            65 Jun 17 21:52 AUTHELIA_STORAGE_ENCRYPTION_KEY
  -rw-------    1 root     root            65 Jun 17 21:52 POSTGRES_PASSWORD

Alright. I think I'll go back to the custom entrypoint.sh idea.
I got it working! Here's my entrypoint.sh:

.. code-block::

  #!/bin/sh

  mkdir -p /my
  cp -r /run/secrets /my/secrets
  chown 1000:1000 /my/secrets/*
  exec su-exec 1000:1000 "$@"

Note that I did get that weird error again, but I opened a new tab and went back in and I stayed logged in.
So, I think it's working better? Idk. It's working.

Now I just need to configure Caddy to put authelia in front of services I need protected.

* https://www.authelia.com/integration/proxies/caddy/
* https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#trusted_proxies
  
I followed the documentation and got it working. 
That error still keeps popping up, so maybe I overengineered the solution to a non-existant problem.
But, it is working right now, so I won't change anything.
Worth noting I am using ``trusted_proxies 172.16.0.0/16`` to basically say I trust anything coming from my docker containers.
This might not be the most secure thing ever, so I might try to change it later.
(Maybe I could give authelia a static IP and only trust that particular IP rather than an entire subnet).
I mean, if I run ``docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' authelia`` 
I get ``172.18.0.25``, which is actually on a different subnet. Maybe I don't even need trusted proxies?
Yeah, let's remove it. I think trusted proxies is only for the cases where you want to completely bypass authentication, but I don't want to do that.
Logging in and redirection is a little janky, but at least I only have to login once.

I didn't have a perfect time setting up authelia, but it seems to get the job done for now.
Maybe I'll go back to authentik eventually. But authelia is nice and simple for now.

June 18 - Authelia is giving me Problems
---------------------------------------------

I must not have configured Authelia correctly.
Upon logging in I am prompted to login multiple times.
When I finally am logged in, I must go to the URL with my service manually (redirect does not work).
Once I get to my service, the page is usually blank, but a reload will finally let me in.

I had looked into Authentik originally, decided it was too complex.
I have heard of Keycloak, but it seems even more overkill than Authentik.
I have now started researching `Caddy Security <https://authp.github.io/>`_, which seems to integrate with Caddy perfectly, as it is a Caddy plugin.

Time to try Caddy Security
------------------------------------------------

It seems like https://blog.sjain.dev/caddy-sso/ is a tutorial that describes exactly what I want to do.

Before I try to configure this, I need to get Caddy Security installed on my Caddy running in a Docker container.
It seems that `Delver26/docker-caddy-security <https://github.com/Delver26/docker-caddy-security>`_ has an image that that is based off of the official caddy image.
`The official caddy image <https://hub.docker.com/_/caddy>`_ as has instructions for extending Caddy that does the same thing.
Also worth noting there are `many other modules <https://caddyserver.com/download>`_ to check out.
Here's my basic Dockerfile:

.. code-block::

  FROM caddy:builder AS builder

  # more modules available here: https://caddyserver.com/download
  # caddy-security releases: https://github.com/greenpau/caddy-security/releases
  RUN xcaddy build --with github.com/greenpau/caddy-security@v1.1.19


  FROM caddy:latest

  LABEL org.opencontainers.image.title=caddy-with-security
  LABEL org.opencontainers.image.description="Caddy with caddy-security module"
  LABEL maintainer="retrodaredevil"

  COPY --from=builder /usr/bin/caddy /usr/bin/caddy

Got it running just like nothing has changed, so now it's time to actually use the caddy-security module.
I didn't realize how easy it would be to create my own Dockerfile and add modules to it.
I'm also glad that compose can easily build the image automatically. I just have to make sure I update it every once in a while.
After some basic configuring from following the tutorial, I had my users.json file automatically generated.
I used the secret found in the logs as my password to login under the user webadmin.
I then navigated manually to the ``/settings/password/edit`` endpoint to change my password.
After some fiddling with my Caddyfile to correct some errors, I now can access some of my services normally.
However, it seems I get forbidden for all of my services now... I get ``user role is valid, but not allowed by access list`` in the logs.
I had to change ``allow roles authp/user`` to ``allow roles authp/admin``, as my webadmin user did not have the user role!

Everything works smoothly!
I might figure out how to change the username of webadmin to lavender later (or add a new user), but for now this is great!
There's no more glitchy login pages!

