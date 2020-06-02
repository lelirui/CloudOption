import subprocess
import re

class CloudDisk():
    def __init__(self):
        self.ceph_osd_list = []
        self.HostIPList = None
        self.DiskInfoDictList = []

    def ceph_osd_position(self):
        local_osd_position_sub = subprocess.Popen(
            ['/opt/bingocloud/latest/output/bin/bingocloud', 'run', 'all', 'ls', '/var/lib/ceph/osd'],
            stdout=subprocess.PIPE)
        local_osd_position_sub.wait()
        local_osd_position = local_osd_position_sub.stdout.read()
        local_osd_position = str(local_osd_position, encoding="utf-8")
        local_osd_position_list = local_osd_position.split('\n')
        local_osd_position_list.pop()
        local_osd_position_dict = {}
        osd_list = []
        hostdict = {}
        for i in range(len(local_osd_position_list)):
            if len(local_osd_position_list[i]) > 20:
                osd_list.append(local_osd_position_list[i].split(' ')[2])
            elif re.search('\%', local_osd_position_list[i]):
                pass
            elif local_osd_position_list[i].split('-')[-1].isdigit():
                osd_list.append('osd.' + local_osd_position_list[i].split('-')[-1])

        osddriversub = subprocess.Popen(
            ['/opt/bingocloud/latest/output/bin/bingocloud run all lsblk | grep sd | grep -v part'], shell=True,
            stdout=subprocess.PIPE)
        osddriversub.wait()
        osddriver = osddriversub.stdout.read()
        osddriver = str(osddriver, encoding="utf-8")
        osdfriverList = osddriver.split('\n')

        ceph_osd_child = subprocess.Popen(['ceph', 'osd', 'df'], stdout=subprocess.PIPE)
        ceph_osd_child.wait()
        ceph_osd_result = ceph_osd_child.stdout.read()
        ceph_osd_result = str(ceph_osd_result, encoding="utf-8")
        # print ceph_osd_result
        ceph_osd_list = ceph_osd_result.split('\n')
        ceph_osd_list.pop()
        del ceph_osd_list[0]
        ceph_osd_list.pop()
        ceph_osd_list.pop()

        systemdisksub = subprocess.Popen(
            ["/opt/bingocloud/latest/output/bin/bingocloud run all df / |  grep /dev |awk  '{print $1"','"$(NF-1)}'"],
            shell=True, stdout=subprocess.PIPE)
        systemdisksub.wait()
        systemdisk = systemdisksub.stdout.read()
        systemdisk = str(systemdisk, encoding="utf-8")
        systemdisk = systemdisk.split('\n')
        systemdisk.pop()
        print(systemdisk)

        ceph_osd = []
        for i in range(len(ceph_osd_list)):
            ceph_osd_list_index = ceph_osd_list.pop()
            ceph_osd_list_index = re.sub(r'\s+', ',', ceph_osd_list_index, count=0)
            ceph_osd_list_index_list = ceph_osd_list_index.split(',')
            if ceph_osd_list_index_list[0] is '':
                del ceph_osd_list_index_list[0]
            ceph_osd.append(ceph_osd_list_index_list)


        for i in range(len(osd_list)):
            if len(osd_list[i])>10:
                self.ceph_osd_list.append(osd_list[i])
                print(systemdisk[0])
                self.ceph_osd_list.append(systemdisk[0].split(' ')[-1].split('%')[0])
                self.ceph_osd_list.append(systemdisk[0].split(' ')[0])
                del systemdisk[0]
                continue
            for j in range(len(ceph_osd)):
                if ceph_osd[j][0] == osd_list[i].split('.')[-1]:
                    self.ceph_osd_list.append(osd_list[i])
                    self.ceph_osd_list.append(ceph_osd[j][-4])
            for j in range(len(osdfriverList)):
                osddriver = osdfriverList[j]
                if osddriver.split(' ')[-1] is '':
                    continue
                if osddriver.split(' ')[-1].split('/')[-1].split('-')[-1] == osd_list[i].split('.')[-1]:
                    self.ceph_osd_list.append('/dev/' + osddriver.split(' ')[0])
        print(self.ceph_osd_list)

    def HostDisk(self,hostip):
        DiskInfoList = []
        strdisk='/opt/bingocloud/latest/output/bin/bingocloud run '+hostip+' /opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL > /tmp/'+hostip+'.disk'
        diskfile = '/tmp/' + hostip + '.disk'
        disk_info=subprocess.Popen(strdisk,shell=True)
        disk_info.wait()

        diskgroupsub = subprocess.Popen('grep DISK ' + diskfile, shell=True, stdout=subprocess.PIPE)
        diskgroupsub.wait()
        diskgroup = diskgroupsub.stdout.read()
        diskgroup = str(diskgroup, encoding="utf-8")
        diskgroupList = diskgroup.split('\n')

        del diskgroupList[0]

        Raidsub = subprocess.Popen('grep "RAID Level" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        Raidsub.wait()
        Raid = Raidsub.stdout.read()
        Raid = str(Raid, encoding="utf-8")
        RaidList = Raid.split('\n')

        VirtDisksub = subprocess.Popen('grep "Virtual Drive" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        VirtDisksub.wait()
        VirtDiskId = VirtDisksub.stdout.read()
        VirtDiskId = str(VirtDiskId, encoding="utf-8")
        VirtDiskIdList = VirtDiskId.split('\n')

        PhysicalDisksub = subprocess.Popen('grep "Physical Disk" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        PhysicalDisksub.wait()
        PhysicalDisk = PhysicalDisksub.stdout.read()
        PhysicalDisk = str(PhysicalDisk, encoding="utf-8")
        PhysicalDiskList = PhysicalDisk.split('\n')
        PhysicalDiskList.pop()

        SlotNumsub = subprocess.Popen('grep "Slot Number" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        SlotNumsub.wait()
        SlotNum = SlotNumsub.stdout.read()
        SlotNum = str(SlotNum, encoding="utf-8")
        SlotNumList = SlotNum.split('\n')

        DeviceIdsub = subprocess.Popen('grep "Device Id" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        DeviceIdsub.wait()
        DeviceId = DeviceIdsub.stdout.read()
        DeviceId = str(DeviceId, encoding="utf-8")
        DeviceIdList = DeviceId.split('\n')

        DiskStatussub = subprocess.Popen('grep "state" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        DiskStatussub.wait()
        DiskStatus = DiskStatussub.stdout.read()
        DiskStatus = str(DiskStatus, encoding="utf-8")
        DiskStatusList = DiskStatus.split('\n')

        ErrorDisksub = subprocess.Popen('grep "Error" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        ErrorDisksub.wait()
        ErrorDisksub = ErrorDisksub.stdout.read()
        ErrorDisksub = str(ErrorDisksub, encoding="utf-8")
        ErrorDisksubList = ErrorDisksub.split('\n')
        del ErrorDisksubList[0]

        RaidDirvesNumsub = subprocess.Popen('grep "Number Of Drives" ' + diskfile, shell=True, stdout=subprocess.PIPE)
        RaidDirvesNumsub.wait()
        RaidDirvesNum = RaidDirvesNumsub.stdout.read()
        RaidDirvesNum = str(RaidDirvesNum, encoding="utf-8")
        RaidDirvesNumList = RaidDirvesNum.split('\n')

        DiskChartsub = subprocess.Popen('ls -l /dev/disk/by-path/ | grep sd | grep -v part|cut -d " " -f11,13',
                                        shell=True, stdout=subprocess.PIPE)
        DiskChartsub.wait()
        DiskChart = DiskChartsub.stdout.read()
        DiskChart = str(DiskChart, encoding="utf-8")
        DiskChartList = DiskChart.split('\n')

        for i in range(len(diskgroupList) - 1):
            DiskInfoList_tmp = []
            DiskInfoDict = {'DISKGROUP': diskgroupList[i].split(' ')[-1]}
            RaidLevel = RaidList[i].split(' ')[12].split('-')[-1].split(',')[0]
            DiskInfoDict.update({'RAIDLevel': RaidLevel})
            VirtDiskId = VirtDiskIdList[2 * i + 1].split(' ')[2]
            DiskInfoDict.update({'VirtualDrive': VirtDiskId})
            for DirChartIn in range(len(DiskChartList) - 1):
                if DiskChartList[DirChartIn].split(' ')[0].split(':')[-2] == VirtDiskId:
                    DiskInfoDict.update(
                        {'DeviceChart': '/dev/' + DiskChartList[DirChartIn].split(' ')[-1].split('/')[-1]})
                    break

            # DiskInfoList_tmp.append(DiskInfoDict)
            # if RaidLevel == '1':
            #     DiskInfoList_tmp.append(DiskInfoDict.copy())
            # elif RaidLevel == '5':
            #     for h in range(4):
            #         DiskInfoList_tmp.append(DiskInfoDict.copy())

            tmp = 0

            for j in range(len(PhysicalDiskList)):


                if j == 0 and re.search('Information', PhysicalDiskList[j]):
                    continue
                elif j != 0 and re.search('Information', PhysicalDiskList[j]):
                    break
                else:
                    DiskInfoList_tmp.append(DiskInfoDict.copy())
                    DiskInfoList_tmp[tmp].update({'PhysicalDisk': PhysicalDiskList[j].split(' ')[-1]})

                    DiskInfoList_tmp[tmp].update({'SlotNum': SlotNumList[0].split(' ')[-1]})
                    del SlotNumList[0]
                    DiskInfoList_tmp[tmp].update({'DeviceId': DeviceIdList[0].split(' ')[-1]})
                    del DeviceIdList[0]
                    DiskStatusDan = DiskStatusList[0].split(',')[-1]
                    DiskStausDan = DiskStatusList[0].split(',')[0].split(' ')[-1]
                    DiskInfoList_tmp[tmp].update({'DiskStaus': DiskStausDan + DiskStatusDan})
                    del DiskStatusList[0]
                    DiskInfoList_tmp[tmp].update({'MediaError': ErrorDisksubList[0].split(' ')[-1]})
                    del ErrorDisksubList[0]
                    DiskInfoList_tmp[tmp].update({'OtherError': ErrorDisksubList[0].split(' ')[-1]})
                    del ErrorDisksubList[0]
                    tmp = tmp + 1

            DiskInfoList.append(DiskInfoList_tmp)
            for k in range(j):
                del PhysicalDiskList[0]
        return DiskInfoList

    def GetHostIp(self):
        HostIpsub = subprocess.Popen(['cat /opt/bingocloud/latest/output/config/deploy-bin/hosts'], shell=True,
                                     stdout=subprocess.PIPE)
        HostIpsub.wait()
        HostIP = HostIpsub.stdout.read()
        HostIP = str(HostIP, encoding="utf-8")
        self.HostIPList = HostIP.split('\n')

    def GetDiskInfo(self):
        ceph_osd_index = []
        for ip in self.HostIPList:
            DiskInfoList = self.HostDisk(ip)
            for i in range(len(DiskInfoList)):
                if len(DiskInfoList[i]) > 0:
                    for j in range(len(DiskInfoList[i])):
                        hostname = ip + '_' + DiskInfoList[i][j]['DeviceId'] + '_' + DiskInfoList[i][j][
                            'SlotNum'] + '_' + DiskInfoList[i][j]['DeviceChart'] + '_' + DiskInfoList[i][j]['RAIDLevel']
                        hostdict = {'hostip': ip, 'hostname': hostname,
                                    'DeviceChart': DiskInfoList[i][j]['DeviceChart'],
                                    'SlotNum': DiskInfoList[i][j]['SlotNum'],
                                    'DeviceId': DiskInfoList[i][j]['DeviceId'],
                                    'DiskStaus': DiskInfoList[i][j]['DiskStaus'],
                                    'MediaError': DiskInfoList[i][j]['MediaError'],
                                    'OtherError': DiskInfoList[i][j]['OtherError']}
                        self.DiskInfoDictList.append(hostdict)
                else:
                    hostname = ip + '_' + DiskInfoList[i][j]['DeviceId'] + '_' + DiskInfoList[i][j]['SlotNum'] + '_' + \
                               DiskInfoList[i][j]['DeviceChart'] + '_' + DiskInfoList[i][j]['RAIDLevel']
                    hostdict = {'hostip': ip, 'hostname': hostname, 'DeviceChart': DiskInfoList[i][j]['DeviceChart'],
                                'SlotNum': DiskInfoList[i][j]['SlotNum'], 'DeviceId': DiskInfoList[i][j]['DeviceId'],
                                'DiskStaus': DiskInfoList[i][j]['DiskStaus'],
                                'MediaError': DiskInfoList[i][j]['MediaError'],
                                'OtherError': DiskInfoList[i][j]['OtherError']}
                    self.DiskInfoDictList.append(hostdict)

            ceph_osd_index.append(self.ceph_osd_list.index(ip))

        ceph_osd_index.append(len(self.ceph_osd_list))
        for i in range(len(ceph_osd_index) - 1):
            step = (ceph_osd_index[i + 1] - ceph_osd_index[i]) / 3
            j = ceph_osd_index[i]
            while j < ceph_osd_index[i + 1]:
                for index in range(len(self.DiskInfoDictList)):
                    if self.DiskInfoDictList[index]['hostip'] == self.ceph_osd_list[ceph_osd_index[i]] and \
                                    self.DiskInfoDictList[index]['DeviceChart'] == self.ceph_osd_list[j + 2]:
                        self.DiskInfoDictList[index].update({'use': self.ceph_osd_list[j + 1]})
                        if j != ceph_osd_index[i]:
                            self.DiskInfoDictList[index].update({'osd': self.ceph_osd_list[j]})
                j = j + 3

    def GetDiskInfoDictList(self):
        return self.DiskInfoDictList