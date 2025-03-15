# use my kali image
FROM kali:2017.1
# disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
# set permissions on tmp directory
RUN mkdir -p /tmp && chmod 1777 /tmp
# add GPG key
RUN curl -fsSL https://archive.kali.org/archive-key.asc | apt-key add -
# fix sources.list
RUN echo "deb http://old.kali.org/kali moto main non-free contrib" > /etc/apt/sources.list
# install required build dependencies
RUN apt-get update && apt-get install -y \
    git build-essential \
    && rm -rf /var/lib/apt/lists/*
# clone, build and install openssl 1.0.1f
RUN git clone -b ubuntu/utopic-devel https://git.launchpad.net/ubuntu/+source/openssl /tmp/openssl && \
    cd /tmp/openssl && \
    ./config no-shared --prefix=/usr/local/ssl --openssldir=/usr/local/ssl && \
    make && make install_sw
# remove pre-installed version of openssl and link vulnerable version
RUN rm -f /usr/bin/openssl
RUN ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
# get heartleech
RUN git clone https://github.com/robertdavidgraham/heartleech.git /opt/heartleech
# set workdir
WORKDIR /opt/heartleech
# compile heartleech with openssl libraries
RUN gcc /opt/heartleech/heartleech.c /usr/local/ssl/lib/libssl.a /usr/local/ssl/lib/libcrypto.a -ldl -lpthread -o /opt/heartleech/heartleech -I/usr/local/ssl/include
# remove unnecessary packages to clean up the image
RUN apt-get purge -y git build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /opt/heartleech/.git
# set entrypoint
ENTRYPOINT ["/opt/heartleech/heartleech"]