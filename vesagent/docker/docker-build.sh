#!/bin/bash
# Copyright (c) 2017-2018 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo "WORKSPACE: ${WORKSPACE}"
VERSION="1.0.0-SNAPSHOT"
STAGING="1.0.0-STAGING"

#
# Copy configurations directory
#
CONF_DIR=${WORKSPACE}/vesagent/etc

if [ ! -d "${CONF_DIR}" ]
then
    echo "FATAL error cannot locate ${CONF_DIR}"
    exit 2
fi

APP_DIR=${WORKSPACE}/vesagent/docker/opt

[ -d "${APP_DIR}/etc" ] && rm -rf "${APP_DIR}/etc"

cp -a ${CONF_DIR} ${APP_DIR}

#
# Copy python scripts directory
#
PY_DIR=${WORKSPACE}/vesagent/py

if [ ! -d "${PY_DIR}" ]
then
    echo "FATAL error cannot locate ${PY_DIR}"
    exit 2
fi

if [  -d "${PY_DIR}" ]
then
    [ -d "${APP_DIR}/py" ] && rm -rf "${APP_DIR}/py"

    cp -a ${PY_DIR} ${APP_DIR}

    echo "Remove all dummy & test scripts"
    rm -f ${APP_DIR}/py/dummy*
    rm -f ${APP_DIR}/py/test*
fi

#
# build the docker image. tag and then push to the remote repo
#
BUILD_ARGS="--no-cache"
DOCKER_REPOSITORY="nexus3.onap.org:10003"
ORG="onap"
PROJECT="multicloud"
IMAGE="vio-vesagent"
VERSION="${VERSION//[^0-9.]/}"
IMAGE_NAME="${DOCKER_REPOSITORY}/${ORG}/${PROJECT}/${IMAGE}"

if [ $HTTP_PROXY ]; then
    BUILD_ARGS+=" --build-arg HTTP_PROXY=${HTTP_PROXY}"
fi
if [ $HTTPS_PROXY ]; then
    BUILD_ARGS+=" --build-arg HTTPS_PROXY=${HTTPS_PROXY}"
fi

function build_image {
    # build the image
    echo "Start build docker image: ${IMAGE_NAME}"
    cd ${WORKSPACE}/vesagent/docker/
    docker build ${BUILD_ARGS} -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${STAGING} .
}

function push_image {
    # push the image
    echo "Start push docker image: ${IMAGE_NAME}"
    docker push ${IMAGE_NAME}:${VERSION}
    docker push ${IMAGE_NAME}:latest
    docker push ${IMAGE_NAME}:${STAGING}
}

build_image
push_image
