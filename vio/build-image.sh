#!/bin/bash

IMAGE="multicloud-vio"
VERSION="latest"

docker build -t ${IMAGE}:${VERSION}
