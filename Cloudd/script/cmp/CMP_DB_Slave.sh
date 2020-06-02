mkfs.ext4 /dev/vdb 2> /dev/null
mkdir /apps
echo "$(blkid /dev/vdb | awk '{print $2}') /apps ext4 defaults 0 0" >> /etc/fstab

mount -a

ntpdate BCC_IP && hwclock -w
echo 'ntpdate BCC_IP && hwclock -w' >> /etc/rc.d/rc.local
echo '0 6 * * * root ntpdate BCC_IP && hwclock -w' >> /etc/crontab