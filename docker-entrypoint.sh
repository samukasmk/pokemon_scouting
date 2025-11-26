#!/bin/sh
set -e

# define variables
INSTANCE_PATH="${INSTANCE_PATH:-/app/instance}"
DB_FILE="$INSTANCE_PATH/pokemon.db"

# ensure instance directory exists and is writable by api user
mkdir -p "$INSTANCE_PATH"

# create file if not exists
if ! [ -e "$DB_FILE" ] ; then
  touch "$DB_FILE"
fi

# fix owner to internal access inside container
chown -R api:api "$INSTANCE_PATH"

# allow permissions to external access
chmod -R 0777 "$INSTANCE_PATH"

# execute docker command with user: api (7777)
exec gosu api "$@"
