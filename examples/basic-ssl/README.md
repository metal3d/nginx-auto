# Example using generated certificates

This example will start a Ghost blog and a reverse proxy responding to `blog.localhost`. Because there is no provided `CERTS` environment for this domain, an internal certificate and key will be generated at startup. Serving SSL/TLS on "https" scheme is activated becasue `SSL` is set to `true`.

The `REDIRECT` environment will make the web browser to be redirected to `https` version of the file.

This means that your web browser should say that the connexion is not sure, but SSL/TLS will be used anyway (you'll need to "continue anyway")

To start the example, type `docker-compose up` then visit http://blog.localhost (you will be redirected to https://docker.localhost)

To remove the example, type `docker-compose down`
