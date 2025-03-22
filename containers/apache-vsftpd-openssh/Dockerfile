# use ubuntu 16.04
FROM ubuntu:16.04
# Set DEBIAN_FRONTEND to noninteractive to prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
# copy openssh server version 7.2p2-4ubuntu2.2 package to container for installation
COPY src/ /tmp/
# install apache2, vsftpd, openssh
RUN apt-get update && apt-get install -y \
    apache2 vsftpd /tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
# run setup
COPY config/startup.sh /
# change permissions
RUN chmod +x /startup.sh
# expose ports
EXPOSE 20 21 22 80 30030 30031 30032 30033 30034 30035
# run startup script
ENTRYPOINT ["/startup.sh"]