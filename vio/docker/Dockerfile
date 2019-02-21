FROM python:2

ENV MSB_ADDR "127.0.0.1"
ENV MSB_PORT "80"
ENV AAI_ADDR "aai.api.simpledemo.openecomp.org"
ENV AAI_PORT "8443"
ENV AAI_SCHEMA_VERSION "v13"
ENV AAI_USERNAME "AAI"
ENV AAI_PASSWORD "AAI"
ENV MR_ADDR "127.0.0.1"
ENV MR_PORT "3904"

EXPOSE 9004

RUN apt-get update && \
    apt-get install -y unzip && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y redis-server

RUN groupadd -r onap && useradd -r -g onap onap

RUN  cd /opt/ && \
    wget -q -O multicloud-vio.zip 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.multicloud.openstack.vmware&a=multicloud-openstack-vmware&v=1.3.0-SNAPSHOT&e=zip' && \
    unzip multicloud-vio.zip && \
    rm -rf multicloud-vio.zip && \
    pip install -r vio/requirements.txt && \
    chown onap:onap -R vio/

USER onap

WORKDIR /opt
# ENTRYPOINT vio/docker/docker-entrypoint.sh
CMD ["/bin/sh", "-c", "/opt/vio/run.sh"]
