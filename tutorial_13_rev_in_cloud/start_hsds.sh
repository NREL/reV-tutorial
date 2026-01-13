#!/bin/bash
# shellcheck disable=SC2155
#
# Install and start a local NREL Public Data Service with HSDS.
# Ubuntu 24.04
# Online Data Browser:
#     https://data.openei.org/s3_viewer?bucket=nrel-pds-hsds&prefix=nrel


# Set the location of the HSDS code directory
export HSDS_DIR=$HOME

# Get this instance's ID and type (with Instance Meta Data Service (IMDS) V2 below, comment out and use V1 below if needed)
export TOKEN=$(curl --silent -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
export EC2_ID=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
export EC2_TYPE=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type)

# Get the ID and Type using IMDS V1
# export EC2_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
# export EC2_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)


# Define Docker checking and installation functions
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
    sudo apt update

    # Run this convenient docker installation script
    curl https://get.docker.com | sudo sh

    # Update groups
    sudo groupadd docker
    sudo usermod -aG docker "$USER"
}

# Stop server if requested
if [[ $1 == "--stop" ]]; then
    echo "Stopping HSDS server."
    cd $HSDS_DIR/hsds
    ./runall.sh --stop
    exit 0
fi

# Start script with first message to user
thisfile=$(realpath $0)
echo "Running $thisfile on $EC2_ID ($EC2_TYPE) from $HSDS_DIR..."

# First check to see if HSDS is running
check_hsds
if [ "$hsds_running" = true ]; then
    # We're good to go
    echo HSDS service running: $hsds_running
    exit 0
else
    # Clone HSDS repository if not found
    if [ ! -d $HSDS_DIR/hsds ]; then
        echo "$HSDS_DIR not found, cloning https://github.com/HDFGroup/hsds.git..."
        git clone https://github.com/HDFGroup/hsds.git
        cd $HSDS_DIR/hsds
    fi

    # Install Docker if not found
    if type docker &>/dev/null; then
        echo "Docker found."
    else
        echo "Docker not found, installing..."
        install_docker
    fi

    # Second check if HSDS is running, start it if not
    check_hsds
    if [ "$hsds_running" = false ]; then
        # Double check that Docker is running
        echo "HSDS not running, starting docker service..."
        sudo service docker start

        # Start HSDS
        echo "Starting local HSDS server..."
        cd $HSDS_DIR/hsds  || exit 1
        ./runall.sh "$(nproc --all)"
    else
        echo HSDS service running: $hsds_running
    fi

    # Give HSDS a chance to warm up (not sure why but this helps a ton!)
    sleep 5s

fi

# One more test to make sure it's actually working
test_fpath="/nrel/wtk/conus/wtk_conus_2010.h5"
test=$(hsls /nrel/wtk/conus/wtk_conus_2010.h5 | grep windspeed_10m)
echo "Running HSDS access test on $test_fpath..."
if [[ $test == "windspeed_10m Dataset {8760, 2488136}" ]]; then
    echo "Windspeed data access test PASSED"
else
    echo "Windspeed data access test FAILED"
fi
state=$(hsinfo | grep "server state")
uptime=$(hsinfo | grep "up:" | cut -d":" -f2)
echo "HSDS $state, uptime: $uptime"
