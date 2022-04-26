# Example using custom certificates

Start a Ghost blog with your own certificates.

This example demonstrate how to use your own local certificates. The Makefile only creates certificates with the very simple tool named `mkcert` https://github.com/FiloSottile/mkcert that is very cool to have a trusted local certificate on your current browser. You'll need to restart your web browser if you never used `mkcert` before or if you tried the previous example (basic-ssl).

The current docker-compose file mounts `./certs` to the `/etc/nginx/certs` volume where nginx will check certificates and keys.

We use `CERTS` variable to apply the corresponding certificate and key to `blog.localhost`.

In details:

- `DOMAINS=blog.localhost:blog:2368` means that nginx will be configured to proxy `blog.localhost` to the `blog` container(s) on port `2368` which is the Ghost blog port
- `CERTS=blog.localhost:cert.pem:key.pem` means that nginx will use `certs.pem` and `key.pem` from the `/etc/nginx/certs` directory to secure connexion on `blog.localhost`
- `SSL=true` activates SSL (optionnal because we use `REDIRECT`)
- `REDIRECT=true` forces web browser to be redirected to https

To start the container with trusted certificates, type `make` - it will create a `./certs` directory with configured certificate and key inside. Then visit `http://blog.localhost`

`make down` will remove the containers and `./certs` directory.
