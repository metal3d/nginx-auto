# Very simple automatic reverse proxy

Nginx-auto is an automatic reverse proxy for Docker and Podman, without configuration file and working with (automatic or not) SSL/TLS.

It's basically made for development usage.

And it's a good companion of `mkcert`.

# Usage

This image is based on `nginx:alpine`, but the entrypoint will make a standard configuration to be a reverse proxy to whatever you need. 

> You don't need configuration files.

This is the environment you can use:

- `DOMAINS` is a **comma separated list** of `domain_name:container[:port]` - e.g.
`DOMAINS=foo.localhost:website1,bar.localhost:another:1234`
- `SSL` if set to `true` (string) so nginx will listens on `443` and use (self generated or not) certificate and keys. (see the [basic ssl example](https://github.com/metal3d/nginx-auto/examples/basic-ssl) for a preview)
- `CERTS` is a **coma separated list** of `domain_name:certname:keyname` where:
    - `certname` is the filename **without direcotry**
    - `keyname` is the filename **without directory**
    You'll need to mount your certificates inside `/etc/nginx/certs` (see [the basic SSL example with trusted certificates here](https://github.com/metal3d/nginx-auto/examples/basic-ssl-trust) for a basic example)
- `REDIRECT` if set to `true` (string) will force http to https redirection


# Basic example

You can see it in [the provided basic example](https://github.com/metal3d/nginx-auto/examples/basic):

```yaml
version: "3"

services:
  blog:
    image: ghost
    environment:
      url: http://blog.localhost

  http:
    image: metal3d/nginx-auto:1.16-alpine
    environment:
      DOMAINS: blog.localhost:blog:2368
    depends_on:
      - blog
    ports:
      - 80:80

```

You can add `SSL: "true"` to activate SSL and why not `REDIRECT: "true"` to force redirection to https.

If you have created your own certificates (e.g. with mkcert) in the form:

- `./certs/foo.bar.key`
- `./certs/foo.bar.pem`

So, your `CERTS` variable should be: `blog.localhots:foo.bar.pem:foo.bar.key` and you must mount `./certs` to `/etc/nginx/certs` (please, use `:z` suffix to make it working even on SELinux systems)

# Work with podman?

Traefik doesn't works with podman (yet) but anyway it will **never** work with **rootless** containers because Traefik (I love it) will use Docker/Podman API that can only work with a "daemon" or "socket". 

> And actually, I made `nginx-auto` to resolve this...

NGinx-auto doesn't use Docker/Podman API, everything works with Environment Variable. Yes, that needs a bit more of typing (or not), but there is no label to use, no specific configuration to activate certificates, and that will work great with [docker-domains](https://github.com/metal3d/docker-domains)

The only thing to change for Podman is to allow "standard user" to open port < 1024:

```
# one shot
sudo sysctl -w net.ipv4.ip_unprivileged_port_start=0

# it you want to make it permanent:
echo 'net.ipv4.ip_unprivileged_port_start=0' | sudo tee /etc/sysctl.d/99-unprivileged_port.conf
sudo systctl --system
```

Now, you can use `podman-compose` and say good bye to Docker :)
