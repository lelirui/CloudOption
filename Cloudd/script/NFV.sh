service bcsm start
chkconfig bcsm on
sed -i '/^ssoBaseEndpoint/d' /etc/bingocloud/nfv-config.properties
echo "ssoBaseEndpoint = ssopoint" >> /etc/bingocloud/nfv-config.properties
systemctl enable mariadb
systemctl start mariadb
systemctl enable tomcat 2> /root/tomcat.log
systemctl restart tomcat