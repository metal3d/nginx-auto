""" Configure nginx for given environment"""
import os

import jinja2
from jinja2.loaders import BaseLoader

TPL = """
{% if ssl or redirect %}
server {
    listen 443 ssl;
    server_name {{ name }};
    ssl_certificate {{ cert }};
    ssl_certificate_key {{ key }};
    location / {
        proxy_pass http://{{ to }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
{% endif %}

{% if redirect %}
server {
    listen 80;
    server_name {{ name }};
    location / {
        return 301 https://$server_name$request_uri;
    }
}
{% endif %}

{% if not ssl and not redirect %}
server {
    listen 80;
    server_name {{ name }};
    location / {
        proxy_pass http://{{ to }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
{% endif %}
"""

# load the TPL template
RENDERER = jinja2.Environment(loader=BaseLoader()).from_string(TPL)

# CERT_PATH to store certificates
if os.environ.get("TEST", False) == "true":
    CERT_PATH = "./certs"
else:
    CERT_PATH = "/etc/nginx/certs"


def main():
    """Main function that does the job"""

    if not os.path.exists(CERT_PATH):
        os.makedirs(CERT_PATH, exist_ok=True)

    domains = os.environ.get("DOMAINS", "").split(",")
    redirect = os.environ.get("REDIRECT", "") == "true"
    ssl = os.environ.get("SSL", "") == "true"
    certs = os.environ.get("CERTS", "").split(",") or []
    # certs=os.environ['CERTS'].split(',')
    for domain in domains:
        name, servername = domain.split(":", 1)
        print("Configuring nginx for {}".format(name))
        # cert = certs[domains.index(domain)]
        # find certificate for this domain in certs
        cert = certs[domains.index(domain)]
        key = ""
        if ssl:
            if cert is None or cert == "":
                # call mkcert to generate a new certificate
                cert = "{}/{}.pem".format(CERT_PATH, name)
                key = "{}/{}.key".format(CERT_PATH, name)
                print("Generating new certificate for {}".format(name))
                os.system(
                    "mkcert -cert-file {} -key-file {} {}".format(cert, key, name)
                )
            else:
                # use given certificate from environment
                try:
                    _, cert, key = cert.split(":")
                    cert = "{}/{}".format(CERT_PATH, cert)
                    key = "{}/{}".format(CERT_PATH, key)
                except ValueError as error:
                    # in this case, we have only one cert and no key, so there is a problem
                    raise ValueError(
                        "Invalid certificate for {}".format(name)
                        + " - we need both cert and key"
                    ) from error
                else:
                    print("Using existing certificate for {}".format(name))

        # render the template
        result = RENDERER.render(
            name=name,
            to=servername,
            redirect=redirect,
            ssl=ssl,
            cert=cert,
            key=key,
        )
        # save or display
        if os.environ.get("TEST", False) == "true":
            print(result)
        else:
            with open("/etc/nginx/conf.d/{}.conf".format(name), "w") as conf_file:
                conf_file.write(result)


if __name__ == "__main__":
    main()
