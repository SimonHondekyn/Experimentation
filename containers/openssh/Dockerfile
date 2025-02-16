# use ubuntu 16.04
FROM ubuntu:16.04
# set env
ENV DEBIAN_FRONTEND=noninteractive
# copy openssh server version 7.2p2-4ubuntu2.2 package to container for installation
COPY src/ /tmp/
# install openssh server version 7.2p2-4ubuntu2.2
RUN apt-get update && apt-get install -y /tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
# copy basic configuration script
COPY config/setup.sh /var/tmp/setup.sh
# change permissions and run basic configuration script
RUN chmod +x /var/tmp/setup.sh && /var/tmp/setup.sh
# run sshd (add -e option to see logs)
CMD ["/usr/sbin/sshd", "-D", "-e"]