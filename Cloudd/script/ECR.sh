sed -i "s/10.202.70.18/sso_ip/g"  /usr/libexec/bingocloud-init-ecr
mkfs.xfs -f /dev/vdb
echo "$(blkid /dev/vdb | awk '{print $2}') /data xfs defaults 0 0" >> /etc/fstab
mount -a
/etc/init.d/ecr stop 2> /root/ectstop.log
/etc/init.d/ecr start 2> /root/ecrstart.log