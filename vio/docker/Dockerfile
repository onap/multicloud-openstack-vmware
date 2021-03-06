FROM python:3-alpine

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

RUN addgroup -S onap && adduser -S -G onap onap

COPY ./multicloud-openstack-vmware-*.zip /opt/multicloud-vio.zip
RUN apk update && \
    apk add uwsgi unzip wget curl gcc make libc-dev libffi-dev openssl-dev && \
    cd /opt/ && \
    # wget -q -O multicloud-vio.zip 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.multicloud.openstack.vmware&a=multicloud-openstack-vmware&v=1.4.2-SNAPSHOT&e=zip' && \
    unzip multicloud-vio.zip && \
    rm -rf multicloud-vio.zip && \
    pip3 install -r /opt/vio/requirements.txt && \
    pip3 install -r /opt/vio/pecan-requirements.txt && \
    mkdir -p /var/log/onap/multicloud/vio && \
    chmod a+rw /var/log/onap/multicloud/vio && \
    chown onap:onap -R /opt/vio/ && \
    apk del unzip gcc make libc-dev libffi-dev openssl-dev

USER onap

WORKDIR /opt/vio
CMD ["/bin/sh", "-c", "/opt/vio/run.sh"]
