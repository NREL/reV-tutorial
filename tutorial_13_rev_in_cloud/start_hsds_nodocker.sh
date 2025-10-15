#!/bin/bash
# shellcheck disable=SC2155
#
# Install and start a local NREL Public Data Service with HSDS.
# Ubuntu 22.04
# Online Data Browser:
#     https://data.openei.org/s3_viewer?bucket=nrel-pds-hsds&prefix=nrel
#
# Note, this is just running the server directly. No docker or any other
# container. This is not the way to do it. You won't be able to spin up and
# shutdown the HSDS server easily. The reason for it is a pressing deadline
# and a particularly pesky authentication error when running through docker.
# Once it's up it's up, the only way I've found to shut it down is by rebooting
# the instance. Hopefully, this won't matter since the compute nodes will only
# run user processes for the duration of their use.

# Log to file
if [ "$1" == "logfile" ]; then
    logfpath="/scratch/hsds_start_logs/test_server_$HOSTNAME-$BASHPID.txt"
    exec 3>&1 1>$logfpath 2>&1
fi

# Get this instance's ID and type (with Instance Meta Data Service (IMDS) V2 below, comment out and use V1 below if needed)
export TOKEN=$(curl --silent -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
export EC2_ID=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
export EC2_TYPE=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type)

# Get the ID and Type using IMDS V1
# export EC2_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
# export EC2_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)

# Print precise datatime string for logging
datetime () {
    date +"%Y-%m-%d %H:%M:%S.%3N"
}

echo "Running reV Job: $REV_JOB_NAME"

thisfile=$(realpath $0)
echo "$(datetime): Running $thisfile on $EC2_ID ($EC2_TYPE)..."

# Define HSDS process checker
check_hsds () {
    hsds_running=false
    if command -v hsds &>/dev/null; then
        echo "$(datetime): HSDS present on system."
        info=$(curl --silent $HSDS_ENDPOINT/info)
        if [[ "$info" == *"READY"* ]]; then
            echo "$(datetime): HSDS is running."
            hsds_running=true
        else
            echo "$(datetime): HSDS is not running."
        fi
    fi
}

# First check to see if HSDS is running
check_hsds
if [ "$hsds_running" = true ]; then
    # We're good to go
    echo "$(datetime): HSDS service detected as running, but waiting 15 seconds to make sure it's totally running."
    sleep 15s
    exit 0
else
    # We need to setup the service
    # Lock this file so only one process on any EC2 hardware can run it
    echo "$(datetime): HSDS not detected as running, but it could be in a startup process..."
    lockfile=/var/lock/start_hsds_$EC2_ID.flock
    thisfile=$(realpath $0)
    exec 200>$lockfile || exit 1  # Originally I had trouble using a double digit file descriptor, but after some tweaking it appears to work
    flock -x -w 600 200 || { echo "ERROR: flock() failed." >&2; exit 1; }

    echo "$(datetime): Locking $thisfile with $lockfile..."

    # Wait for a bit 
    echo "$(datetime): Waiting 15 seconds to ensure HSDS has started..."
    sleep 15s

    # Second check to if HSDS is running, start it if not
    check_hsds
    if [ "$hsds_running" = false ]; then
        # Start HSDS
        echo "$(datetime): HSDS not running, starting local HSDS server..."
        hsds --count "$(nproc --all)" &

        # Wait for a bit 
        echo "$(datetime): Waiting 15 seconds to ensure HSDS has started..."
        sleep 15s

    else
        # We're good to go
        echo "$(datetime): HSDS service detected as running, but waiting 15 seconds to make sure it's totally running."
        sleep 15s
        exit 0
    fi

    # Release the lock on this file (Not necessary unless further steps are added)
    echo "$(datetime): Releasing lock on $thisfile"
    flock -u 200
fi
