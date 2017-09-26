#!/bin/bash
echo "WORKSPACE: ${WORKSPACE}"
VERSION="1.0.0-SNAPSHOT"

#
# Copy vesagent Uber JAR to docker app directory
#
APP=${WORKSPACE}/vesagent/target/vesagent-${VERSION}.jar

if [ ! -f "${APP}" ]
then
    echo "FATAL error cannot locate ${APP}"
    exit 2
fi

APP_DIR=${WORKSPACE}/vesagent/docker/opt

[ -d "${APP_DIR}/vesagent-${VERSION}.jar" ] && rm -rf "${APP_DIR}/vesagent-${VERSION}.jar"

cp ${APP} ${APP_DIR}

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

APP_DIR=${WORKSPACE}/vesagent/docker/opt

[ -d "${APP_DIR}/py" ] && rm -rf "${APP_DIR}/py"

cp -a ${PY_DIR} ${APP_DIR}

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
    docker build ${BUILD_ARGS} -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest .
}

function push_image {
    # push the image
    echo "Start push docker image: ${IMAGE_NAME}"
    docker push ${IMAGE_NAME}:${VERSION}
    docker push ${IMAGE_NAME}:latest
}

build_image
push_image
