#!/bin/bash

which mysqld 2> /root/isMysql
if cat /root/isMysql | grep no 1>/dev/null;then wget http://169.254.169.254:8683/common/mysql-5.0.1.zip -P /root 2>/dev/null; unzip /root/mysql-*.zip -d /root;sh /root/mysql/install.sh --type cluster  -p pass@word1 --passwd bingocloud localIp 2>&1 ;fi
which java 2> /root/isjava
if cat /root/isjava | grep no 1> /dev/null;then yum install -y java-1.8.0-openjdk ;fi

echo "CREATE DATABASE iam CHARACTER SET utf8 COLLATE utf8_general_ci;" > /root/iam.sql
mysql -ubingocloud -pbingocloud < /root/iam.sql 2> /dev/null

wget http://169.254.169.254:8683/common/iam_20190807-17.08.zip -P /root 2>/dev/null
unzip /root/iam_*.zip -d /root
mkdir -p /opt/dist/sso
mkdir -p /opt/dist/console
mkdir -p /opt/dist/iamapi
mkdir -p /opt/dist/iamuser

unzip /root/dist/sso.zip -d /opt/dist/sso
unzip /root/dist/console.zip -d /opt/dist/console
unzip /root/dist/iamapi.zip -d /opt/dist/iamapi
unzip /root/dist/iamuser.zip -d /opt/dist/iamuser

sed -i 's/url: /url: "jdbc:mysql:\/\/localIp:3306\/iam?characterEncoding=UTF-8"/g' /opt/dist/sso/conf/application.yml
sed -i 's/username: /username: bingocloud/g' /opt/dist/sso/conf/application.yml


sed -i '/redis/d' /opt/dist/sso/conf/application.yml
sed -i '/hostAndPort/d' /opt/dist/sso/conf/application.yml
sed -i '/sentinelHostAndPorts/d' /opt/dist/sso/conf/application.yml
sed -i '/sentinelMasterName/d' /opt/dist/sso/conf/application.yml
sed -i '/sentinelMasterName/d' /opt/dist/sso/conf/application.yml
sed -i '/password/d' /opt/dist/sso/conf/application.yml
sed -i '4  a\  password: bingocloud'  /opt/dist/sso/conf/application.yml
sed -i "$ a\  context-path: /sso"   /opt/dist/sso/conf/application.yml

chmod a+x /opt/dist/sso/bin/*
/opt/dist/sso/bin/sso start
sleep 20
if ss -atnl | grep 8089 >/dev/null;then echo 'true';else sleep 10;fi

sed -i 's/url: /url: "jdbc:mysql:\/\/localIp:3306\/iam?characterEncoding=UTF-8"/g' /opt/dist/console/conf/application.yml
sed -i 's/username: /username: bingocloud/g' /opt/dist/console/conf/application.yml
sed -i 's/password: /password: bingocloud/g' /opt/dist/console/conf/application.yml
sed -i 's/client: /client: iamapp/g' /opt/dist/console/conf/application.yml
sed -i 's/secret: /secret: iamapp/g' /opt/dist/console/conf/application.yml
sed -i 's/server: /server: http:\/\/localIp:8089\/sso/g' /opt/dist/console/conf/application.yml
sed -i "$ a\  context-path: /console" /opt/dist/console/conf/application.yml

echo "use iam;" > /root/console.sql
echo "INSERT INTO oauth2_user (id , user_name, password, need_change_password, allow_authorize_clients, admin, name, job_title, email, mobile, e_code, granted_scope, active) VALUES ('1', 'approve_admin', '$2a$10$cvnJlzIMe7HuoiglBKtEkueYI8FgGoBUTxVx00hTEAbpgtxJV0SIy', 0, '', 1, '审批管理员', NULL, 'approve@local', NULL, 'local', 'iam_admin', 1);" >> /root/console.sql
echo "INSERT INTO idm_user_role (id, user_id, role_id, app_id, created_at, created_by, updated_at, updated_by, __meta__) VALUES ('1', '1', '0', 'iam', '2019-07-24 15:39:55', NULL, '2019-07-24 15:39:55', NULL, '{}');" >> /root/console.sql

mysql -ubingocloud -pbingocloud < /root/console.sql 2>/dev/null
chmod a+x /opt/dist/console/bin/*
/opt/dist/console/bin/console  start


sed -i 's/url: /url: "jdbc:mysql:\/\/localIp:3306\/iam?characterEncoding=UTF-8"/g' /opt/dist/iamapi/conf/application.yml
sed -i 's/username: /username: bingocloud/g' /opt/dist/iamapi/conf/application.yml
sed -i 's/password: /password: bingocloud/g' /opt/dist/iamapi/conf/application.yml
sed -i 's/client: /client: iamapp/g' /opt/dist/iamapi/conf/application.yml
sed -i 's/secret: /secret: iamapp/g' /opt/dist/iamapi/conf/application.yml
sed -i 's/server: /server: http:\/\/localIp:8089\/sso/g' /opt/dist/iamapi/conf/application.yml
sed -i "$ a\  context-path: /iamapi" /opt/dist/iamapi/conf/application.yml

chmod a+x /opt/dist/iamapi/bin/*
/opt/dist/iamapi/bin/iamapi  start