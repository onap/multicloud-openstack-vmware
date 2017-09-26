# Use an official Python runtime as a parent image
FROM python:2.7.14

# Make port <Port Num> available to the world outside this container
#EXPOSE <Port Num>

RUN echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get update && \
    apt-get install -y vim && \
    apt-get install -y zip && \
    apt-get install -y unzip && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y -t jessie-backports openjdk-8-jre-headless ca-certificates-java

# Set the working directory to /opt
WORKDIR /opt

# Copy the local opt directory contents into the container at /opt
ADD opt /opt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run application when the container launches
CMD [ "/opt/start-manager.sh" ]
