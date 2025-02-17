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
# expose port(s)
EXPOSE 20 21 30030 30031 30032 30033 30034 30035
# run vsftpd
CMD ["/usr/sbin/vsftpd"]