mkfs.ext4 /dev/vdb 2> /dev/null
mkdir /apps
echo "$(blkid /dev/vdb | awk '{print $2}') /apps ext4 defaults 0 0" >> /etc/fstab

mount -a

ntpdate BCC_IP && hwclock -w
echo 'ntpdate BCC_IP && hwclock -w' >> /etc/rc.d/rc.local
echo '0 6 * * * root ntpdate BCC_IP && hwclock -w' >> /etc/crontab
curl http://169.254.169.254:8683/common/ > /root/s3.txt 2>/dev/null
sed -i 's/<Key>/\n/g' /root/s3.txt
sed -i 's/<\/Key>/\n/g' /root/s3.txt
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep cmp)  -P /root 2> /dev/null
unzip /root/bingocmp-3.*.zip -d /root
unzip /root/com-4.*.zip -d /root > /root/comunzip.txt 2>&1
cd /root/com_pkgs_original_new_arch/com_zabbix/;sh zabbix-db_install.sh > /root/install.test 2>&1
cd /root/com_pkgs_original_new_arch/com_zabbix/;sh import_zabbix_db.sh >> /root/install.test 2>&1
cd /root/com_pkgs_original_new_arch/com_zabbix/;sh zabbix-server_install.sh >> /root/install.test 2>&1
cd /root/com_pkgs_original_new_arch/database/import_monitor_db/;sh import_monitor_db.sh >> /root/install.test 2>&1
