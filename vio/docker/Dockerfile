FROM python:2

ENV MSB_ADDR "127.0.0.1"
ENV MSB_PORT "80"
ENV AAI_ADDR "aai.api.simpledemo.openecomp.org"
ENV AAI_PORT "8443"
ENV AAI_SCHEMA_VERSION "v11"
ENV AAI_USERNAME "AAI"
ENV AAI_PASSWORD "AAI"

EXPOSE 9004

RUN apt-get update && \
    apt-get install -y unzip && \
    apt-get install -y curl && \
    apt-get install -y wget


RUN  cd /opt/ && \
    wget -q -O multicloud-vio.zip 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.multicloud.openstack.vmware&a=multicloud-vio&v=LATEST&e=zip' && \
    unzip multicloud-vio.zip && \
    rm -rf multicloud-vio.zip && \
    pip install -r vio/requirements.txt


WORKDIR /opt
ENTRYPOINT vio/docker/docker-entrypoint.sh
