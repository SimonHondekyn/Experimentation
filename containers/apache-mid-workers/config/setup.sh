#!/bin/bash

echo "ListenBacklog 100" >> /etc/apache2/apache2.conf
sed -i '/<IfModule mpm_event_module>/a \        ServerLimit 7' /etc/apache2/mods-available/mpm_event.conf
sed -i 's/^\(\s*\)ThreadsPerChild\s*[0-9]\+/\1ThreadsPerChild 5/' /etc/apache2/mods-available/mpm_event.conf
sed -i 's/^\(\s*\)MaxRequestWorkers\s*[0-9]\+/\1MaxRequestWorkers 35/' /etc/apache2/mods-available/mpm_event.conf

a2dismod mpm_prefork
a2enmod mpm_event