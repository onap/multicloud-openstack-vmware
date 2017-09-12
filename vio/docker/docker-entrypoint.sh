#!/bin/bash


if [ -z "$SERVICE_IP" ]; then
    export SERVICE_IP=`hostname -i`
fi
echo
echo Environment Variables:
echo "SERVICE_IP=$SERVICE_IP"

if [ -z "$MSB_ADDR" ]; then
    echo "Missing required variable MSB_ADDR: Microservices Service Bus address <ip>:<port>"
    exit 1
fi
echo "MSB_ADDR=$MSB_ADDR"
echo


echo

# Configure service based on docker environment variables
vio/docker/instance-config.sh


# Perform one-time config
if [ ! -e init.log ]; then

    # microservice-specific one-time initialization
    vio/docker/instance-init.sh

    date > init.log
fi

# Start the microservice
vio/docker/instance-run.sh
