import subprocess

class CloudDiskNum():
    def CloudOSDNum(self):
        CephOsdSub = subprocess.Popen(
            ["ceph osd df | awk '{print $1}' | wc -l"], shell=True,
            stdout=subprocess.PIPE)
        CephOsdSub.wait()
        CephOsd = CephOsdSub.stdout.read()
        CephOsd = str(CephOsd, encoding="utf-8")
        CephOsdList = CephOsd.split('\n')
        CephOsdList.pop()
        return int(CephOsdList[0])

    def CloudDiskSum(self):
        DiskSumSub = subprocess.Popen([
                                       "/opt/bingocloud/latest/output/bin/bingocloud run all /opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL | grep 'Physical Disk:' | wc -l"],
                                   shell=True, stdout=subprocess.PIPE)
        DiskSumSub.wait()
        DiskSum = DiskSumSub.stdout.read()
        DiskSum = str(DiskSum, encoding="utf-8")
        DiskSumList = DiskSum.split('\n')
        DiskSumList.pop()
        return int(DiskSumList[0])

    def CloudErrorSum(self):
        CloudMetidaSub = subprocess.Popen([
                                       "/opt/bingocloud/latest/output/bin/bingocloud run all /opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL | grep 'Media Error'"],
                                   shell=True, stdout=subprocess.PIPE)
        CloudMetidaSub.wait()
        CloudMetida = CloudMetidaSub.stdout.read()
        CloudMetida = str(CloudMetida, encoding="utf-8")
        CloudMetidaList = CloudMetida.split('\n')
        CloudMetidaList.pop()


        CloudOtherSub = subprocess.Popen([
                                       "/opt/bingocloud/latest/output/bin/bingocloud run all /opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL | grep 'Other Error'"],
                                   shell=True, stdout=subprocess.PIPE)
        CloudOtherSub.wait()
        CloudOther = CloudOtherSub.stdout.read()
        CloudOther = str(CloudOther, encoding="utf-8")
        CloudOtherList = CloudOther.split('\n')
        CloudOtherList.pop()

        error = 0
        for i in range(len(CloudMetidaList)):
            if int(CloudMetidaList[i].split(':')[-1]) != 0 or int(
                    CloudOtherList[i].split(':')[-1]) != 0:
                error = error + 1
        return error
