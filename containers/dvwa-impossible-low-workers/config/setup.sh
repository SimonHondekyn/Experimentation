#!/bin/bash

set -e

echo "ListenBacklog 128" >> /etc/apache2/apache2.conf
sed -i 's/^\(\s*\)MaxRequestWorkers\s*[0-9]\+/\1MaxRequestWorkers 35/' /etc/apache2/mods-available/mpm_prefork.conf

chown -R www-data:www-data /var/www/html/dv
chmod -R 755 /var/www/html/dv

echo "Starting MySQL..."
service mysql start

echo "Waiting for MySQL to be ready..."
while ! mysqladmin ping -h localhost --silent; do
    sleep 2
done

mysql -u root <<EOF
USE mysql;
UPDATE user SET plugin='mysql_native_password' WHERE user='root';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
EOF

mysql -u root -proot < /var/www/mysql_init.sql
rm -f /var/www/mysql_init.sql

echo "Starting Apache in foreground..."
exec apache2ctl -D FOREGROUND