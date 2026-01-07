#!/bin/bash
# shellcheck disable=SC2155
#
# Install and start a local NREL Public Data Service with HSDS.
# Ubuntu 24.04
# Online Data Browser:
#     https://data.openei.org/s3_viewer?bucket=nrel-pds-hsds&prefix=nrel


export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
export BUCKET_NAME="nrel-pds-hsds"
export AWS_REGION="us-west-2"
export AWS_S3_GATEWAY="http://s3.us-west-2.amazonaws.com/"
export HSDS_ENDPOINT="http://localhost:5102"
export LOG_LEVEL="ERROR"
export ROOT_DIR="/scratch/hsdsdata"
export AWS_S3_NO_SIGN_REQUEST=1

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
    if command -v docker &>/dev/null; then
        echo "HSDS present on system."
        if [[ $(docker ps | wc -l) -ge 5 ]]; then
            echo "HSDS is running."
            hsds_running=true
        fi
    fi
}

install_docker () {
    # Update repositories
    sudo apt-get update

    # Install the package
    sudo apt install docker.io docker-compose -y

    # Enable and start the docker background service
    sudo systemctl start docker
    sudo systemctl enable docker

    # Update permissions and groups
    sudo chmod 666 /var/run/docker.sock
    sudo chmod +x /usr/local/bin/docker-compose
    sudo groupadd docker
    sudo usermod -aG docker "$USER"
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
    exec 9>$lockfile || exit 1  # Ubuntu doesn't allow double digit file descriptors by default, apparently, whereas other OSs do (someone email me and explain me this)
    flock -x -w 600 9 || { echo "ERROR: flock() failed." >&2; exit 1; }
    echo "Locking $thisfile with $lockfile..."

    # Install Docker if not found
    if type docker &>/dev/null; then
        echo "Docker found."
    else
        echo "Docker not found, installing..."
        install_docker
    fi

    # Second check to if HSDS is running, start it if not
    check_hsds
    if [ "$hsds_running" = false ]; then
        # Double check that Docker is running
        echo "HSDS not running, starting docker service..."
        sudo chmod 666 /var/run/docker.sock
        sudo groupadd docker
        sudo usermod -aG docker "$USER"
        sudo service docker start

        # Start HSDS
        echo "Starting local HSDS server..."
        cd ~/hsds || exit
        ./runall.sh "$(nproc --all)"
        cd - || exit
    else
        echo HSDS service running: $hsds_running
    fi

    # Give HSDS a chance to warm up (not sure why but this helps a ton!)
    sleep 10s

    # Release the lock on this file (Not necessary unless further steps are added)
    echo "Releasing lock on $thisfile"
    flock -u 9

fi