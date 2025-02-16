#!/bin/bash

mkdir -p /var/run/vsftpd/empty
chown root:root /var/run/vsftpd/empty
chmod 755 /var/run/vsftpd/empty

useradd -m -s /bin/bash iscxtap
echo "iscxtap:1234" | chpasswd

chown root:root /home/iscxtap
chmod 755 /home/iscxtap
mkdir /home/iscxtap/ftp
chown iscxtap:iscxtap /home/iscxtap/ftp
chmod 755 /home/iscxtap/ftp

echo "port_enable=NO" >> /etc/vsftpd.conf
echo "pasv_enable=YES" >> /etc/vsftpd.conf
echo "pasv_min_port=30030" >> /etc/vsftpd.conf
echo "pasv_max_port=30035" >> /etc/vsftpd.conf
echo "local_umask=022" >> /etc/vsftpd.conf
sed -i "s/^#\?listen=.*/listen=YES/" /etc/vsftpd.conf
sed -i "s/^#\?listen_ipv6=.*/listen_ipv6=NO/" /etc/vsftpd.conf
sed -i "s/^#\?write_enable.*/write_enable=YES/" /etc/vsftpd.conf
sed -i "s/^#\?xferlog_file.*/xferlog_file=\/var\/log\/vsftpd.log/" /etc/vsftpd.conf
sed -i "s/^#\?chown_uploads.*/chown_uploads=YES/" /etc/vsftpd.conf
sed -i "s/^#\?chroot_local_user.*/chroot_local_user=YES/" /etc/vsftpd.conf