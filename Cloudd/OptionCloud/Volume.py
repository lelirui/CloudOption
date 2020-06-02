import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'OptionCloud'))
from util import xmltodict,cloudutil
from OptionCloud import Cloude
class VolumeOption():
    def __init__(self,client):
        self.client=client

    def CreateVolume(self,ServiceIMC,Size):
        ClodeInfo=Cloude.ClodeInfo(self.client)
        params={"VolumeName":ServiceIMC+'Volume',"availabilityZone":ClodeInfo.getClusterName(),"Size":Size}
        
        result = self.client.invoke("CreateVolume", params)
        CreateResult=xmltodict.parse(result,encoding='utf-8')
        return CreateResult['CreateVolumeResponse']['volumeId']


    def DelVolume(self,VolumeId):
        params={"IsInstanceVol":False,"VolumeId":VolumeId}
        result = self.client.invoke("DeleteVolume", params)
        DelVolumeResult=xmltodict.parse(result, encoding='utf-8')
        return DelVolumeResult["DeleteVolumeResponse"]["return"]

    def Instance_Vloume(self,ImageId,VolumeId,DervicePosition='/dev/vdb'):
        params={"VolumeId":VolumeId,"InstanceId":ImageId,"Device":DervicePosition,'MountPoint':"","DeleteOnTermination":False,
                "Cache":"default","isOneInst":False}
        result=self.client.invoke("AttachVolume",params)
        return result
