#!/bin/bash

echo "ListenBacklog 128" >> /etc/apache2/apache2.conf
sed -i 's/^\(\s*\)MaxRequestWorkers\s*[0-9]\+/\1MaxRequestWorkers 100/' /etc/apache2/mods-available/mpm_event.conf

a2dismod mpm_prefork
a2enmod mpm_event