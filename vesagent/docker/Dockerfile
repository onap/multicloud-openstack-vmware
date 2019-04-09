# Use an official Python runtime as a parent image
FROM python:2-alpine

# Make port <Port Num> available to the world outside this container
#EXPOSE <Port Num>

# Set the working directory to /opt
WORKDIR /opt

# Copy the local opt directory contents into the container at /opt
ADD opt /opt

RUN apk update && \
    apk add zip unzip curl wget openjdk8 && \
    cd /opt/ && \
    wget -O /opt/vesagent-1.0.0.jar 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.multicloud.openstack.vmware&a=vesagent&v=LATEST&e=jar' && \
    pip install -r requirements.txt && \
    apk del zip unzip

# Run application when the container launches
CMD [ "/opt/start-manager.sh" ]
