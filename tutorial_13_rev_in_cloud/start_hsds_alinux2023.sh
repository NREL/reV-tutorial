#!/bin/bash
# shellcheck disable=SC2155
#
# Install and start a local NREL Public Data Service with HSDS.
# Amazon Linux 2023
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

# Get this instances ID and Type (with  Instance Meta Data Service (IMDS) v2 below, comment out and use v1 below if needed)
export TOKEN=$(curl --silent -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
export EC2_ID=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
export EC2_TYPE=$(curl --silent -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type)

# Get the ID and Type using IMDS v1
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


# First check to see if HSDS is running
check_hsds
if [ "$hsds_running" = true ]; then
    echo HSDS service running: $hsds_running
else
    (
        # We need to setup the service
        # Lock this file so only one process on any EC2 hardware can run it
        flock -x -w 600 200 || exit 1

        # Install docker if not found
        if ! command -v docker &> /dev/null; then
            sudo dnf install -y docker
            sudo systemctl start docker
            sudo chmod 666 /var/run/docker.sock
        fi

        # Install docker-compose if not found
        if ! command -v docker-compose &> /dev/null; then
            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
        fi

        # Second check to if HSDS is running, start it if not
        check_hsds
        if [ "$hsds_running" = false ]; then
            # Double check that Docker is running
            sudo chmod 666 /var/run/docker.sock
            sudo groupadd docker
            sudo usermod -aG docker "$USER"
            sudo service docker start

            # Start HSDS
            echo Starting HSDS local server...
            cd ~/hsds/ || exit
            sh runall.sh "$(nproc --all)"
            cd - || exit
        else
            echo HSDS service running: $hsds_running
        fi

        # Give HSDS a chance to warm up (not sure why but this helps a ton!)
        sleep 10s

    ) 200>/tmp/.rev_ec2_"$EC2_ID".flock
fi
