sed -i '/^ssoBaseEndpoint/d' /etc/web.properties
echo "ssoBaseEndpoint = ssopoint" >> /etc/web.properties
sed -i 's/C0A0E0C6C896FEF26A10/sdnAccessKey/g' /etc/web.properties
sed -i 's/[W][a-zA-Z0-9]*[d]$/sdnSecurityKey/g' /etc/web.properties
/opt/apache-tomcat-8.5.24/bin/shutdown.sh 2> /root/TomcatShutdown.log
sleep 5
/opt/apache-tomcat-8.5.24/bin/startup.sh
