#!/bin/bash

mkdir -p /var/run/sshd
chown root:root /var/run/sshd
chmod 700 /var/run/sshd

useradd -m -s /bin/bash iscxtap
echo "iscxtap:1234" | chpasswd

sed -i "s/^#\?PermitRootLogin.*/PermitRootLogin no/" /etc/ssh/sshd_config
sed -i "s/^#\?PasswordAuthentication.*/PasswordAuthentication yes/" /etc/ssh/sshd_config
sed -i "s/^#\?MaxStartups.*/MaxStartups 50:50:100/" /etc/ssh/sshd_config
#sed -i "s/^#\?LogLevel.*/LogLevel VERBOSE/" /etc/ssh/sshd_config