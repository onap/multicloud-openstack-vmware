# Use an official Python runtime as a parent image
FROM python:2.7.14

# Make port <Port Num> available to the world outside this container
#EXPOSE <Port Num>

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y zip && \
    apt-get install -y unzip && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y openjdk-7-jre

# Set the working directory to /opt
WORKDIR /opt

# Copy the local opt directory contents into the container at /opt
ADD opt /opt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD [ "/opt/start-manager.sh" ]
