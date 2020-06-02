sshpass -p 'cloudpass' scp /etc/ceph/ceph.conf root@SVZ_IP:/etc/ceph/  2> /root/sshpass.log
sleep 10
echo "{ceph_watch_url,'http://SVZ_IP:8082'}." >> /opt/bingocloud/latest/output/config/clc.cfg