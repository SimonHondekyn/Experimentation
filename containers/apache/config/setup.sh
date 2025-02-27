#!/bin/bash

a2enmod reqtimeout
echo "RequestReadTimeout header=103" >> /etc/apache2/apache2.conf
sed -i "s/^#\?Timeout.*/Timeout 9999/" /etc/apache2/apache2.conf