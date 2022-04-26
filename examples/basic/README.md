# A basic example

This example starts a Ghost blog container and make it available on http://blog.localhost. There is no SSL/TLS in this example. It only proposes the basic configuration.

- `DOMAINS:blog.localhost:blog:2368` - as Ghost listens `2368` port, nginx will be configured to proxy the connexion to `blog` container(s) on port `2368`.

To start the example, use `docker-compose up`

To remove the example, use `docker-compose down`
