# base image
FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get purge --auto-remove && apt-get clean

# update pip
RUN python -m pip install --upgrade pip --disable-pip-version-check

# set the working dir to /temp
WORKDIR /temp

# copy all
COPY . .
RUN pip install -r src/requirements.txt

# create mountpoint
VOLUME /temp

RUN echo "###############"
RUN coverage run -m unittest discover
