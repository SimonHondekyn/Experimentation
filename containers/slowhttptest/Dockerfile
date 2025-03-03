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
# install the required packages
RUN apt-get update && apt-get install -y --allow-downgrades \
    git build-essential zlib1g=1:1.2.7.dfsg-13 libssl-dev autoconf automake libtool \
    && rm -rf /var/lib/apt/lists/*
# use older version of slowhttptest
RUN git clone https://github.com/shekyan/slowhttptest.git /opt/slowhttptest && \
    cd /opt/slowhttptest && git checkout ccf670f
# set workdir
WORKDIR /opt/slowhttptest
# configure, compile, install
RUN ./configure --prefix=/usr/local && \
    make && make install
# set entrypoint
ENTRYPOINT ["slowhttptest"]