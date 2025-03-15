#!/bin/bash

echo "ListenBacklog 128" >> /etc/apache2/apache2.conf
sed -i 's/^\(\s*\)MaxRequestWorkers\s*[0-9]\+/\1MaxRequestWorkers 100/' /etc/apache2/mods-available/mpm_prefork.conf

chown -R www-data:www-data /var/www/html/dv
chmod -R 755 /var/www/html/dv

service mysql start
sleep 5

mysql -u root <<EOF
USE mysql;
UPDATE user SET plugin='mysql_native_password' WHERE user='root';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
EXIT;
EOF

mysql -u root -p'root' < /var/www/mysql_init.sql
rm -rf /var/www/mysql_init.sql

service mysql stop