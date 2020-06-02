mkfs.ext4 /dev/vdb 2> /dev/null
mkdir /opt/mysql
echo "$(blkid /dev/vdb | awk '{print $2}') /opt/mysql ext4 defaults 0 0" >> /etc/fstab
mount -a
echo 'ntpdate BCC_IP && hwclock -w' >> /etc/rc.local 2>/dev/null

