# use ubuntu 12.04
FROM ubuntu:12.04
# update sources.list
RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
# install openssl and apache2 dependencies
RUN apt-get update && apt-get install -y \
    git build-essential zlib1g-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
# copy openssl 1.0.1f source
COPY src/openssl-1.0.1f.tar.gz /usr/local/src/
# change dir
WORKDIR /usr/local/src
# build and install openssl 1.0.1f
RUN tar -xvzf openssl-1.0.1f.tar.gz && \
    cd openssl-1.0.1f && \
    ./config no-shared --prefix=/usr/local/ssl --openssldir=/usr/local/ssl && \
    make && make install_sw
# remove pre-installed version of openssl and link vulnerable version
RUN rm -f /usr/bin/openssl
RUN ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
# clone apache2 to build from source
RUN git clone -b ubuntu/precise https://git.launchpad.net/ubuntu/+source/apache2 && \
    cd apache2 && \
    ./configure --enable-ssl --with-ssl=/usr/local/ssl && \
    make && make install
# create certificate
RUN openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -sha1 \
    -keyout /usr/local/apache2/conf/server.key \
    -out /usr/local/apache2/conf/server.crt \
    -subj "/C=CA/ST=NB/L=f/O=Internet Widgits Pty Ltd/CN=localhost"
# include ssl configuration
RUN sed -i 's/^#Include conf\/extra\/httpd-ssl.conf/Include conf\/extra\/httpd-ssl.conf/' /usr/local/apache2/conf/httpd.conf
# listen on port 444 instead of 443
RUN sed -i 's/^Listen 443/Listen 444/' /usr/local/apache2/conf/extra/httpd-ssl.conf
RUN sed -i 's/^<VirtualHost _default_:443>/<VirtualHost _default_:444>/' /usr/local/apache2/conf/extra/httpd-ssl.conf
# expose port 444
EXPOSE 444
# run the server in the foreground
CMD ["/usr/local/apache2/bin/apachectl", "-D", "FOREGROUND"]