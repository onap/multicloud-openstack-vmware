FROM python:2

ENV MSB_ADDR "127.0.0.1"
ENV MSB_PORT "80"
ENV AAI_ADDR "aai.api.simpledemo.openecomp.org"
ENV AAI_PORT "8443"
ENV AAI_SCHEMA_VERSION "v11"
ENV AAI_USERNAME "AAI"
ENV AAI_PASSWORD "AAI"

EXPOSE 9004

COPY ./ /opt/vio/
RUN pip install -r /opt/vio/requirements.txt

WORKDIR /opt/vio
CMD /bin/sh -c /opt/vio/run.sh
