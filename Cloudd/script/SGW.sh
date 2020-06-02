service bcsm start
chkconfig bcsm on
sed -i '/^ssoBaseEndpoint/d' /etc/bingosgw/sgw-web.properties
echo "ssoBaseEndpoint = ssopoint" >> /etc/bingosgw/sgw-web.properties
systemctl enable mariadb
systemctl start mariadb
systemctl enable tomcat 2> /root/tomcat.log
systemctl restart tomcat