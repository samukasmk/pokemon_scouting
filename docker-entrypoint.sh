#!/bin/sh
set -e

INSTANCE_PATH="${INSTANCE_PATH:-/app/instance}"

# Ensure instance directory exists and is writable by api user
mkdir -p "$INSTANCE_PATH"
chown -R api:api "$INSTANCE_PATH"
chmod -R 0777 "$INSTANCE_PATH"

exec gosu api "$@"
