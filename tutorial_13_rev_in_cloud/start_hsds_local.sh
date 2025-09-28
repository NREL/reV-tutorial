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

    # Lock this file to make sure only one compute node can run it script per EC2 hardware
    lockfile=/var/lock/start_hsds_$EC2_ID.flock
    thisfile=$(realpath $0)
    exec 9>$lockfile || exit 1  # Ubuntu doesn't allow double digit file descriptors by default, whereas other OSs do (someone email me and explain me this)
    flock -x -w 600 9 || { echo "ERROR: flock() failed." >&2; exit 1; }
    echo "Locking $thisfile with $lockfile..."

    # Install docker if not found
    if type docker &>/dev/null; then
        echo "Docker found."
    else
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
        cd ~/hsds || exit
        ./runall.sh "$(nproc --all)"
        cd - || exit
    else
        echo HSDS service running: $hsds_running
    fi

    # Give hsds a chance to warm up (not sure why but this helps a ton!)
    sleep 10s

    # Release the lock on this file
    echo "Releasing lock on $thisfile"
    flock -u 9

fi