#!/bin/bash

echo "RequestReadTimeout header=100" >> /etc/apache2/apache2.conf
sed -i "s/^#\?Timeout.*/Timeout: 9999/" /etc/apache2/apache2.conf