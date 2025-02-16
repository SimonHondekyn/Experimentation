# use ubuntu 16.04
FROM ubuntu:16.04
# install vsftpd
RUN apt-get update && apt-get install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*
# copy basic configuration script
COPY config/setup.sh /var/tmp/setup.sh
# change permissions and run basic configuration script
RUN chmod +x /var/tmp/setup.sh && /var/tmp/setup.sh
# run vsftpd
CMD ["/usr/sbin/vsftpd"]