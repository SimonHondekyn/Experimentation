#!/bin/bash

#a2enmod reqtimeout
#echo "RequestReadTimeout header=103,minrate=1" >> /etc/apache2/apache2.conf
#sed -i "s/^#\?Timeout.*/Timeout 9999/" /etc/apache2/apache2.conf
#sed -i "s/^#\?MaxRequestWorkers*/MaxRequestWorkers  10/" /etc/apache2/mods-available/mpm_event.conf
echo "ListenBacklog 128" >> /etc/apache2/apache2.conf
sed -i 's/^\s*MaxRequestWorkers\s*[0-9]\+/MaxRequestWorkers 100/' /etc/apache2/mods-available/mpm_event.conf