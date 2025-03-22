# use ubuntu 16.04
FROM ubuntu:16.04
# set environment variables
# prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
# set security level
ENV DVWA_SECURITY_LEVEL=low
# install apache2
RUN apt-get update && apt-get install -y \
    apache2 git mysql-server php php-mysqli php-gd libapache2-mod-php \
    && rm -rf /var/lib/apt/lists/*
# install DVWA v1.10 *Development*
RUN git clone --depth 1 --branch 2.1 https://github.com/digininja/DVWA.git /var/www/html/dv
# copy DVWA and MySQL config, and basic setup
COPY config/config.inc.php /var/www/html/dv/config/
COPY config/mysql_init.sql /var/www/
COPY config/setup.sh /var/tmp/setup.sh
# change permissions and run basic configuration script
RUN chmod +x /var/tmp/setup.sh
# expose port(s)
EXPOSE 80 3306
# run setup script
ENTRYPOINT ["/var/tmp/setup.sh"]