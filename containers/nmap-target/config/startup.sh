#!/bin/bash

set -e

# set up iptables rules for SCTP

# iptables -A INPUT -p sctp -j ACCEPT

# Samba server configuration

useradd -m -s /bin/bash iscxtap
echo "iscxtap:1234" | chpasswd

mkdir /home/iscxtap/samba
chown iscxtap:iscxtap /home/iscxtap/samba
chmod 755 /home/iscxtap/samba

(echo "1234"; echo "1234") | smbpasswd -a iscxtap -s

echo "Starting Samba..."
service smbd start
service nmbd start

# NTP server

echo "Starting NTP..."
service ntp start

# basic apache webserver configuration

echo "ListenBacklog 128" >> /etc/apache2/apache2.conf
sed -i 's/^\(\s*\)MaxRequestWorkers\s*[0-9]\+/\1MaxRequestWorkers 100/' /etc/apache2/mods-available/mpm_event.conf
sed -i 's/^#\?\s*KeepAliveTimeout\s\+[0-9]\+/KeepAliveTimeout 10/' /etc/apache2/apache2.conf

echo "Starting Apache in the background..."
apache2ctl start

# same configuration for this OpenSSH server as before (SSH-Patator)

mkdir -p /var/run/sshd
chown root:root /var/run/sshd
chmod 700 /var/run/sshd

sed -i "s/^#\?PermitRootLogin.*/PermitRootLogin no/" /etc/ssh/sshd_config
sed -i "s/^#\?PasswordAuthentication.*/PasswordAuthentication yes/" /etc/ssh/sshd_config
sed -i "s/^#\?MaxStartups.*/MaxStartups 50:50:100/" /etc/ssh/sshd_config

echo "Starting OpenSSH..."
service ssh start

# same configuration for this vsFTPd server as before (FTP-Patator)

mkdir -p /var/run/vsftpd/empty
chown root:root /var/run/vsftpd/empty
chmod 755 /var/run/vsftpd/empty

chown root:root /home/iscxtap
chmod 755 /home/iscxtap
mkdir /home/iscxtap/ftp
chown iscxtap:iscxtap /home/iscxtap/ftp
chmod 755 /home/iscxtap/ftp

echo "port_enable=NO" >> /etc/vsftpd.conf
echo "pasv_enable=YES" >> /etc/vsftpd.conf
echo "pasv_min_port=30000" >> /etc/vsftpd.conf
echo "pasv_max_port=30050" >> /etc/vsftpd.conf
sed -i "s/^#\?listen.*/listen=YES/" /etc/vsftpd.conf
sed -i "s/^#\?listen_ipv6.*/listen_ipv6=NO/" /etc/vsftpd.conf
sed -i "s/^#\?write_enable.*/write_enable=YES/" /etc/vsftpd.conf
sed -i "s/^#\?local_umask.*/local_umask=022/" /etc/vsftpd.conf
sed -i "s/^#\?xferlog_file.*/xferlog_file=\/var\/log\/vsftpd.log/" /etc/vsftpd.conf
sed -i "s/^#\?chroot_local_user.*/chroot_local_user=YES/" /etc/vsftpd.conf

echo "Starting vsFTPd in foreground..."
/usr/sbin/vsftpd /etc/vsftpd.conf