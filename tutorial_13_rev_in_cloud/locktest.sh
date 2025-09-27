#!/bin/bash
LOCKFILE="/tmp/$FILE.lock"

exec 200>"$LOCKFILE" || exit 1
flock 200

echo "Lock acquired for this file, it will wait for 30 seconds before it completes and releases the file for the next process."

sleep 30

echo "Finished, releasing lock"

flock -u 200

exit 0
