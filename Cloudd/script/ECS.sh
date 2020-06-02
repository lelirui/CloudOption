yum install -y wget 2> /dev/null
curl http://169.254.169.254:8683/common/ > /root/s3.txt 2>/dev/null
sed -i 's/<Key>/\n/g' /root/s3.txt
sed -i 's/<\/Key>/\n/g' /root/s3.txt
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep ecs-web)  -P /root 2> /dev/null
rm -rf /opt/tomcat/webapps/ROOT.war
cp /root/ecs-web-*.war /opt/tomcat/webapps/ROOT.war
sed -i '/^Service.Admin.AccessKeyId/d' /etc/bingoecs/web.properties
sed -i '5iService.Admin.AccessKeyId=accesskey' /etc/bingoecs/web.properties
sed -i '/^Service.Admin.SecurityKey/d' /etc/bingoecs/web.properties
sed -i '6iService.Admin.SecurityKey=securitykey' /etc/bingoecs/web.properties

sed -i '/^Cloud.Endpoint/d' /etc/bingoecs/web.properties
sed -i '9iCloud.Endpoint=endpoint' /etc/bingoecs/web.properties

sed -i '/^API.Endpoint/d' /etc/bingoecs/web.properties
sed -i '16iAPI.Endpoint=endpoint' /etc/bingoecs/web.properties

sed -i '/^ssoBaseEndpoint/d' /etc/bingoecs/web.properties
sed -i '20issoBaseEndpoint=ssoIpaddr' /etc/bingoecs/web.properties

sed -i '/^ecr.web.address/d' /etc/bingoecs/web.properties
sed -i '32iecr.web.address=ecraddress' /etc/bingoecs/web.properties
systemctl restart tomcat  2> /root/ecsstart.log