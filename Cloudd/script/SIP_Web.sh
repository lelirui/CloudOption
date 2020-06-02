mkfs.ext4 /dev/vdb 2> /dev/null
mkdir /bsip
echo "$(blkid /dev/vdb | awk '{print $2}') /bsip ext4 defaults 0 0" >> /etc/fstab
mount -a
echo 'ntpdate BCC_IP && hwclock -w' >> /etc/rc.local 2>/dev/null
curl http://169.254.169.254:8683/common/ > /root/s3.txt 2>/dev/null
sed -i 's/<Key>/\n/g' /root/s3.txt
sed -i 's/<\/Key>/\n/g' /root/s3.txt
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep sip)  -P /root 2> /dev/null
unzip /root/sip4.1-*.zip -d /root
unzip /root/sip-*.zip -d /root
sh /root/sip.web.4.1.*.new.run -h mysqlvip > /root/web.text  2>&1
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep repo)  -P /root 2> /dev/null

unzip /root/repo*.zip -d /bsip/repo