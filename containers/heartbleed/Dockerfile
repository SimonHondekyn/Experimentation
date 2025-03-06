# use ubuntu 12.04
FROM ubuntu:12.04
# set env
ENV DEBIAN_FRONTEND=noninteractive
# update sources.list
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
# install requirements for building openssl version 1.0.1f
RUN apt-get update && apt-get install -y \
    build-essential zlib1g-dev apache2 ssl-cert \
    && rm -rf /var/lib/apt/lists/*
# copy package to container
COPY src/openssl_1.0.1f.orig.tar.gz /usr/local/src/
# set workdir
WORKDIR /usr/local/src
# extract, build, install
RUN tar -xvzf openssl_1.0.1f.orig.tar.gz && \
    cd openssl-1.0.1f && \
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib && \
    make && make install
# first move openssl that comes with apache, then create symlink
RUN mv /usr/bin/openssl /usr/bin/openssl.bak && \
    ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
# enable ssl module
RUN a2enmod ssl
# copy apache configuration to container
COPY config/000-default.conf /etc/apache2/sites-available/000-default.conf
# port 444 is used instead of port 443
EXPOSE 444
# run apache2
CMD ["apache2ctl", "-D", "FOREGROUND"]