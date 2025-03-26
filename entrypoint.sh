#!/bin/bash
set -e

# Set the correct permissions
chown www-data:www-data /tuoteselosteet/db.sqlite3 && chmod 755 /tuoteselosteet/db.sqlite3
chown www-data:www-data /tuoteselosteet && chmod 755 /tuoteselosteet

# Execute the CMD
exec "$@"