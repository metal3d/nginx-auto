from nginx:1.16-alpine

ARG MKCERT_VERSION=v1.4.3

# install mkcert
RUN set -eux;\
    apk add --no-cache \
        python3 py-jinja2 \
        ca-certificates \
        curl \
        gnupg \
        openssl;\
    curl -sSL https://github.com/FiloSottile/mkcert/releases/download/${MKCERT_VERSION}/mkcert-${MKCERT_VERSION}-linux-amd64 -o /usr/local/bin/mkcert; \
    chmod +x /usr/local/bin/mkcert; \
    mkcert -install;

# add our entrypoint
COPY ./entrypoint.sh /entrypoint.sh
COPY ./nginxconf.py /nginxconf.py
RUN set xe; chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# back to normal
EXPOSE 80 443
VOLUME ["/etc/nginx/certs"]
ENV DOMAINS="" CERTS="" SSL=false REDIRECT=false
CMD ["nginx", "-g", "daemon off;"]

