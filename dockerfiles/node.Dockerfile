FROM node:21

WORKDIR /neoinst/frontend

RUN apt-get update  \
    && apt-get upgrade -y

RUN npm install -g npm@10.5.2