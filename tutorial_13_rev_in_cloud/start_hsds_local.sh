#!/bin/bash
# shellcheck disable=SC2155

export AWS_ACCESS_KEY_ID=${YOUR_KEY_ID_HERE}  
export AWS_SECRET_ACCESS_KEY=${YOUR_SECRET_KEY_HERE}
export BUCKET_NAME=${YOUR_BUCKET_NAME_HERE}
export AWS_REGION=us-west-2
export AWS_S3_GATEWAY=http://s3.us-west-2.amazonaws.com/
export HSDS_ENDPOINT=http://localhost:5101
export LOG_LEVEL=INFO
export EC2_ID=SPOOFID

echo Checking HSDS and Docker...


check_hsds () {
    hsds_running=false
    if command -v docker > /dev/null; then
        if [[ $(docker ps | wc -l) -ge 5 ]]; then
            hsds_running=true
        fi
    fi
}

install_docker () {
    # Update repositories
    sudo apt-get update

    # Install the package
    sudo apt install docker.io docker-compose

    # Enable and start the docker background service
    sudo systemctl start docker
    sudo systemctl enable docker

    # Update permissions and groups
    sudo chmod 666 /var/run/docker.sock
    sudo chmod +x /usr/local/bin/docker-compose
    sudo groupadd docker
    sudo usermod -aG docker "$USER"

    # This probably isn't required on EC2?
    sudo gpasswd -a $USER docker
}


# First check to see if HSDS is running
check_hsds
if [ "$hsds_running" = true ]; then
    # We're good to go
    echo HSDS service running: $hsds_running
else
    # Lock this file to make sure only one compute node can run it script per EC2 hardware
    lockfile="/tmp/start_hsds_$EC2_ID.flock"
    exec 200>"$lockfile" || exit 1
    flock -x -w 600 200
    thisfile="$(realpath $0)"
    echo "Locking $thisfile..."

    # Install docker if not found
    if ! command -v docker &> /dev/null; then
        echo "Docker not found, installing..."
        install_docker
    fi

    # Second check if HSDS is running, start it if not
    check_hsds
    if [ "$hsds_running" = false ]; then
        echo "HSDS not running, starting docker service..."
        # Make sure docker is available (if the service stopped or 
        sudo chmod 666 /var/run/docker.sock
        sudo groupadd docker
        sudo usermod -aG docker "$USER"
        sudo service docker start

        # Start HSDS
        echo "Starting local HSDS server..."
        cd ~/github/hsds/ || exit
        sh runall.sh "$(nproc --all)"
        cd - || exit
    else
        echo HSDS service running: $hsds_running
    fi

    # Give hsds a chance to warm up (not sure why but this helps a ton!)
    sleep 10s

    # Release the lock on this file
    echo "Releasing lock on $thisfile"
    flock -u 200

fi

exit 0
