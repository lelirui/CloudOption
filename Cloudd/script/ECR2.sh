mkfs.xfs -f /dev/vdb
echo "$(blkid /dev/vdb | awk '{print $2}') /opt xfs defaults 0 0" >> /etc/fstab
mount -a
yum install ntpdate -y
ntpdate cloudIp && hwclock -w

echo 'ntpdate cloudIp  && hwclock -w' >> /etc/rc.d/rc.local
echo '0 6 * * * root ntpdate cloudIp  && hwclock -w' >> /etc/crontab
systemctl start docker
systemctl enable docker 2> /dev/null
echo '127.0.0.1  registry.bingosoft.net' >> /etc/hosts
wget http://169.254.169.254:8683/common/bingo-harbor.tar -P /root 2> /dev/null
tar -xf /root/bingo-harbor.tar
sed -i '/read/d' /root/bingo-harbor/setup.sh
sed -i 's/response/1/g' /root/bingo-harbor/setup.sh
cd /root/bingo-harbor;sh /root/bingo-harbor/setup.sh y  2>/root/error.log
sed -i 's/registry.bingosoft.net/ecr_ip/g'  /opt/bingo-harbor/harbor.cfg
sed -i 's/https:\/\/sso.bingosoft.net/http:\/\/sso_ip\/sso/g'  /opt/bingo-harbor/harbor.cfg
cd /opt/bingo-harbor; ./docker-compose down --remove-orphans 2>> /root/error.log
cd /root/bingo-harbor;sh update.sh 2>> /root/error.log

crontab -l > harbor_cron 2> harbor_cron.err
echo "*/5 * * * * cd /opt/bingo-harbor && ./docker-compose -f docker-compose.yml -f docker-compose.chartmuseum.yml up -d" >> harbor_cron
crontab harbor_cron
rm harbor_cron