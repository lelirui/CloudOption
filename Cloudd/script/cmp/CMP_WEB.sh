mkfs.ext4 /dev/vdb 2> /dev/null
mkdir /apps
echo "$(blkid /dev/vdb | awk '{print $2}') /apps ext4 defaults 0 0" >> /etc/fstab
mkfs.ext4 /dev/vdc 2> /dev/null
mkdir /bsip
echo "$(blkid /dev/vdc | awk '{print $2}') /bsip ext4 defaults 0 0" >> /etc/fstab

mount -a

ntpdate BCC_IP && hwclock -w
echo 'ntpdate BCC_IP && hwclock -w' >> /etc/rc.d/rc.local
echo '0 6 * * * root ntpdate BCC_IP && hwclock -w' >> /etc/crontab
curl http://169.254.169.254:8683/common/ > /root/s3.txt 2>/dev/null
sed -i 's/<Key>/\n/g' /root/s3.txt
sed -i 's/<\/Key>/\n/g' /root/s3.txt
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep cmp)  -P /root 2> /dev/null
unzip /root/bingocmp-3.*.zip -d /root
unzip /root/sip-4.*.zip -d /root
cp /root/env/cmp_poc_4-hosts.conf /root/env/install.conf

sed -i 's/sip_web_ip =/sip_web_ip =webIp/g' /root/env/install.conf

sed -i 's/sip_db_ip =/sip_db_ip =dbmaster_ip/g' /root/env/install.conf

sed -i 's/^web_ip =/web_ip = webIp/g' /root/env/install.conf

sed -i 's/web_passwd =/web_passwd = pass@word1/g' /root/env/install.conf

sed -i 's/job_interface_ip =/job_interface_ip =jobIp/g'  /root/env/install.conf

sed -i 's/job_interface_passwd =/job_interface_passwd =pass@word1/g' /root/env/install.conf

sed -i 's/basedb_ip =/basedb_ip =db-master_ip/g'  /root/env/install.conf

sed -i 's/basedb_passwd =/basedb_passwd =pass@word1/g' /root/env/install.conf

sed -i 's/zabbix_ip =/zabbix_ip =zabbixip/g' /root/env/install.conf

sed -i 's/zabbix_zabbixdb_ip =/zabbix_zabbixdb_ip =zabbixip/g' /root/env/install.conf

sed -i 's/zabbix_zabbixdb_passwd =/zabbix_zabbixdb_passwd =pass@word1/g' /root/env/install.conf

sed -i 's/monitor_ip =/monitor_ip =zabbixip/g'  /root/env/install.conf

sed -i 's/monitor_passwd =/monitor_passwd =pass@word1/g' /root/env/install.conf

sed -i 's/xxxxxx/pass@word1/g' /root/env/install.conf

sh /root/sip.web.*.new.run > /root/web.text  2>&1
unzip /root/com-4.*.zip -d /root > /root/comunzip.txt 2>&1
cd /root/com_pkgs_original_new_arch/init_scripts/;sh cmp_config_hosts_and_ntp.sh -a dbmaster_ip -z zabbixip -i jobIp > /root/install.test 2>&1
cd /root/com_pkgs_original_new_arch/database/import_base_db/config_zabbix-sip-bcc_for_com/;sh config_zabbix_sip_bcc.sh >> /root/install.test 2>&1
cd /root/com_pkgs_original_new_arch/com_base_standalone/;sh cmp_web_install.sh >> /root/install.test 2>&1

ssh root@CPM_IJ 'cd /root/com_pkgs_original_new_arch/com_base_standalone/;sh cmp_web_service_install.sh'  >> /root/install.test 2>&1

wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep repo)  -P /root 2> /dev/null

unzip /root/repo*.zip -d /bsip/repo
