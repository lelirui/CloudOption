
service bcsm start
chkconfig bcsm on
sed -i 's/ssoBaseEndpoint = /& ssopoint/g' /etc/bingocloud/vas-config.properties
systemctl enable mariadb 2>> /root/vasinstall.log
systemctl start mariadb
systemctl enable tomcat 2>> /root/vasinstall.log
systemctl restart tomcat
chkconfig vas on 2>> /root/vasinstall.log
service vas start