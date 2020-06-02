mkdir /opt/bingoeks 2> /dev/null
sleep 5
mkfs.xfs -f /dev/vdb
echo "$(blkid /dev/vdb | awk '{print $2}') /opt/bingoeks xfs defaults 0 0" >> /etc/fstab
mount -a
systemctl stop eks-agent rexray kubelet 2> /dev/null
systemctl disable eks-agent rexray kubelet 2> /dev/null
mkdir -p /opt/bingoeks/logs
mkdir -p /opt/bingoeks/config
curl http://169.254.169.254:8683/common/ > /root/s3.txt 2>/dev/null
sed -i 's/<Key>/\n/g' /root/s3.txt
sed -i 's/<\/Key>/\n/g' /root/s3.txt
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep bingoeks)  -P /root 2> /dev/null
wget   http://169.254.169.254:8683/common/$(cat s3.txt| grep mysql)  -P /root 2> /dev/null
wget http://169.254.169.254:8683/common/bingoeks.sql -P /root/ 2> /dev/null
wget http://169.254.169.254:8683/common/application.yml -P /root 2> /dev/null
wget http://169.254.169.254:8683/common/eks-docker-images.tar.gz -P /root 2> /dev/null
wget http://169.254.169.254:8683/common/upload_docker_images.sh -P /root 2> /dev/null
wget http://169.254.169.254:8683/common/eks_configs.tar -P /root 2> /dev/null
docker load -i /root/mysql-*.tar
docker load -i /root/bingoeks-*.tar


docker run -d --restart always -v /opt/bingoeks/mysql_data:/var/lib/mysql -e MYSQL_USER=bingoeks -e MYSQL_PASSWORD=pass@bingo_eks -e MYSQL_ROOT_PASSWORD=pass@bingo_eks -e MYSQL_DATABASE=bingoeks --network host --name eks_mysql mysql:5.6

docker cp /root/bingoeks.sql eks_mysql:/tmp/
sleep 20

echo "mysql -ubingoeks -ppass@bingo_eks bingoeks < /tmp/bingoeks.sql" > /root/initsql.sh
chmod a+x /root/initsql.sh
docker cp /root/initsql.sh eks_mysql:/tmp/
docker exec eks_mysql sh /tmp/initsql.sh 2> /root/initsql.log

tar -xf /root/eks_configs.tar
mv /root/eks_configs /opt/bingoeks/

cp /root/application.yml /opt/bingoeks/config/
sed -i 's/password: bingoeks/password: pass@bingo_eks/g' /opt/bingoeks/config/application.yml

sed -i 's/10.201.76.185/sso/g' /opt/bingoeks/config/application.yml
sed -i 's/1A77E8A9A127B30F8124/accessKey/g' /opt/bingoeks/config/application.yml
sed -i 's/WzBEQkQ1Qzc1RjJFRkNBN0I5QzUzQjkzN0QzNUI0REM1N0E3MkY1RDBd/securitykey/g' /opt/bingoeks/config/application.yml

docker run --restart always -d -v /opt/bingoeks/config:/opt/bingoeks/config -v /opt/bingoeks/logs:/opt/bingoeks/logs -v /opt/bingoeks/eks_configs:/opt/bingoeks/eks_configs --network host --name bingoeks registry.bingosoft.net/bingocloud/bingoeks:1.3.$(cat s3.txt  | grep bingoeks- | cut -d '.' -f3)
sleep 20
docker exec eks_mysql sh /tmp/initsql.sh 2> /root/initsql.log