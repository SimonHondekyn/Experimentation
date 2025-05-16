# use ubuntu 16.04
FROM ubuntu:16.04
# Set DEBIAN_FRONTEND to noninteractive to prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
# install apache2
RUN apt-get update && apt-get install -y \
    apache2 \
    && rm -rf /var/lib/apt/lists/*
# run setup
COPY config/setup.sh /var/tmp/setup.sh
# change permissions and run basic configuration script
RUN chmod +x /var/tmp/setup.sh && /var/tmp/setup.sh
# expose port(s)
EXPOSE 80
# run mysql and apache2
CMD ["apache2ctl", "-D", "FOREGROUND"]