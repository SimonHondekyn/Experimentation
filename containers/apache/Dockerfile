# use ubuntu 16.04
FROM ubuntu:16.04
# install apache2
RUN apt-get update && apt-get install -y \
    apache2 \
    && rm -rf /var/lib/apt/lists/*
# copy basic configuration script
COPY config/setup.sh /var/tmp/setup.sh
# change permissions and run basic configuration script
RUN chmod +x /var/tmp/setup.sh && /var/tmp/setup.sh
# expose port(s)
EXPOSE 80
# run apache2
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]