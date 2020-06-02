ceph osd pool create cephfs-data 16 2> /dev/null
ceph osd pool create cephfs-meta 16 2> /dev/null
/opt/bingocloud/latest/output/tools/install/res/common/ceph/install.sh --type mds --metapool cephfs-meta --datapool cephfs-data vip
/opt/bingocloud/latest/output/bin/bingocloud run all wget http://127.0.0.1:81/common/rpms.tar.gz -P /root 2> /dev/null
/opt/bingocloud/latest/output/bin/bingocloud run all tar -zxf /root/rpms.tar.gz
/opt/bingocloud/latest/output/bin/bingocloud run all yum install -y /root/rpms*/*.rpm /root/rpms*/ceph12.2.x/*.rpm
/opt/bingocloud/latest/output/bin/bingocloud run all chkconfig efs-agent on
/opt/bingocloud/latest/output/bin/bingocloud run all service efs-agent start
