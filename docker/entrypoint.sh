#!/bin/sh

# auto configure nginx
python3 /nginxconf.py

# Back to parent entrypoint
[ -f /docker-entrypoint.sh ] && exec /docker-entrypoint.sh "$@"
exec "$@"
