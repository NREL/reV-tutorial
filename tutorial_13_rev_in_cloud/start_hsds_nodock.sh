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

# If you have variables you depend on in your .bashrc, they might not be run in a job submission
export AWS_S3_GATEWAY="http://s3.us-west-2.amazonaws.com/"
export HSDS_ENDPOINT="http://localhost:5101"

# Get this instance's ID and type (with Instance Meta Data Service (IMDS) V2 below, comment out and use V1 below if needed)
export TOKEN=$(curl --silent -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
export EC2_ID=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
export EC2_TYPE=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type)

# Get the ID and Type using IMDS V1
# export EC2_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
# export EC2_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)

thisfile=$(realpath $0)
echo "Running $thisfile on $EC2_ID ($EC2_TYPE)..."

check_hsds () {
    hsds_running=false
    if command -v hsds &>/dev/null; then
        echo "HSDS present on system."
        info=$(curl --silent $HSDS_ENDPOINT/info)
        if [[ "$info" == *"READY"* ]]; then
            echo "HSDS is running."
            hsds_running=true
        fi
    fi
}

# First check to see if HSDS is running
check_hsds
if [ "$hsds_running" = true ]; then
    # We're good to go
    echo HSDS service running: $hsds_running
    exit 0
else
    # We need to setup the service
    # Lock this file so only one process on any EC2 hardware can run it
    lockfile=/var/lock/start_hsds_$EC2_ID.flock
    thisfile=$(realpath $0)
    exec 9>$lockfile || exit 1  # Ubuntu doesn't allow double digit file descriptors by default, apparently, whereas other OSs do (someone email us and explain this)
    flock -x -w 600 9 || { echo "ERROR: flock() failed." >&2; exit 1; }
    echo "Locking $thisfile with $lockfile..."

    # Second check to if HSDS is running, start it if not
    check_hsds
    if [ "$hsds_running" = false ]; then
        # Start HSDS
        echo "HSDS not running, starting local HSDS server..."
        hsds --count "$(nproc --all)" &

        # Give HSDS a chance to warm up (not sure why but this helps a ton!)
        sleep 30s

        # Now let's write a little test file out
        mkdir -p /scratch/tests
        out_fpath=/scratch/tests/test_server_$HOSTNAME.txt
        curl --silent http://localhost:5101/about > $out_fpath
        curl --silent http://localhost:5101/info >> $out_fpath
        echo "\n" >> $out_fpath
    else
        echo HSDS service running: $hsds_running
    fi


    # Release the lock on this file (Not necessary unless further steps are added)
    echo "Releasing lock on $thisfile"
    flock -u 9
fi