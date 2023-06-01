# base image
FROM python:3.11-slim

# apt-get install libgomp1 to prevent lightgbm errors
RUN apt-get update && apt-get upgrade -y && \
    apt-get purge --auto-remove && apt-get clean && \
    apt-get install libgomp1

# update pip
RUN python -m pip install --upgrade pip --disable-pip-version-check

# set the working dir to /temp
WORKDIR /temp

# copy all
COPY src .
RUN pip install -r requirements.txt

# expose port for Jenkins
EXPOSE 8080

# create mountpoint
VOLUME /temp

RUN echo "###############"
RUN python -m unittest
