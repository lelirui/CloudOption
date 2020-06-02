
service bcsm start
chkconfig bcsm on
sed -i '/^ssoBaseEndpoint/d' /etc/bingoefs/efs-web.properties
echo "ssoBaseEndpoint = ssopoint" >> /etc/bingoefs/efs-web.properties
systemctl enable mariadb
systemctl start mariadb
systemctl enable tomcat 2> /root/tomcat.log
systemctl restart tomcat