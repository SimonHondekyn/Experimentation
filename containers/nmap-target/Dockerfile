# use ubuntu 16.04
FROM ubuntu:16.04
# Set DEBIAN_FRONTEND to noninteractive to prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
# copy openssh server version 7.2p2-4ubuntu2.2 package to container for installation
COPY src/ /tmp/
# install apache2, vsftpd, openssh
RUN apt-get update && apt-get install -y \
    apache2 vsftpd samba ntp /tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
# copy script and smb config
COPY config/startup.sh /
COPY config/smb.conf /etc/samba/
# change permissions
RUN chmod +x /startup.sh
# run startup script
ENTRYPOINT ["/startup.sh"]