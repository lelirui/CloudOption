import base64
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import xmltodict,cloudutil


class InstanceOption():
    def __init__(self,client):
        self.client=client

    def run_instance(self,imageId, instanceType, vpcId, subnetId, instanceName, volumeSize, role,InitInstanceData):
        if InitInstanceData is '':

            userData = 'not-ready'
            encodeUserData = base64.b64encode(bytes(userData, 'utf-8'))
        else:
            encodeUserData = base64.b64encode(bytes(InitInstanceData, 'utf-8'))
        params = {"ImageId": imageId, "MinCount": "1", "InstanceType": instanceType, "VpcId": vpcId,
                  "SubnetId": subnetId, "InstanceName": instanceName,
                  "BlockDeviceMapping.1.DeviceName": "/dev/vda", "BlockDeviceMapping.1.Ebs.VolumeSize": volumeSize,
                  "NetworkInterfaces": "3", "UserData": encodeUserData, "iamInstanceProfile.Name": role,"Password":'pass@word1'}
        result = self.client.invoke("RunInstances", params)
        return result

    def getCreateInstanceID(self,imageId, instanceType, vpcId, subnetId, instanceName, volumeSize, role,InitInstanceData):

        Instanceinfo=self.run_instance(imageId, instanceType, vpcId, subnetId, instanceName, volumeSize, role,"")
        XMLInstanceInfo=xmltodict.parse(Instanceinfo,encoding='utf-8')
        return XMLInstanceInfo['RunInstancesResponse']['instancesSet']['item']['instanceId']

    def Instance_Vloume(self,ImageId,VolumeId):
        params={"VolumeId":VolumeId,"InstanceId":ImageId,"Device":"/dev/vdb",'MountPoint':"","DeleteOnTermination":False,
                "Cache":"default","isOneInst":False}
        result=self.client.invoke("AttachVolume",params)
        return result

    def DescribeInstances(self,vpcId,InstanceId):
        params = {"Filter.1.Name": "vpc-id", "Filter.1.Value.1": vpcId, "Filter.2.Name": "instance-id",
                  "Filter.2.Value.1": InstanceId}
        # params = { "Filter.1.Name": "vpc-id", "Filter.1.Value.1": vpcId}
        result=self.client.invoke("DescribeInstances",params)
        return result

    def InstanceXMLIpInfo(self,vpcId,ImageId):
        result=self.DescribeInstances(vpcId,ImageId)
        Instancxml=xmltodict.parse(result,encoding='utf-8')

        # if not Instancxml:
        #     return None
        # try:
        #     v = Instancxml["DescribeInstancesResponse"]["reservationSet"]["item"]
        #     if type(v).__name__ == 'list':
        #         for item in v:
        #             if item["instancesSet"]["item"]["instanceId"] == ImageId and \
        #                             item["instancesSet"]["item"]["vpcId"] == vpcId:
        #                 return item["instancesSet"]["item"]["ipAddress"]
        #         return None
        #     elif type(v).__name__ == 'OrderedDict':
        #         if v["instancesSet"]["item"]["instanceId"] == ImageId and \
        #                         v["instancesSet"]["item"]["vpcId"] == vpcId:
        #             return v["instancesSet"]["item"]["ipAddress"]
        #         return None
        # except Exception as e:
        #     return None

        return Instancxml["DescribeInstancesResponse"]["reservationSet"]["item"]["instancesSet"]["item"]["ipAddress"]


    def DelInstance(self,InstanceId):
        param={"InstanceId":InstanceId}
        result=self.client.invoke("TerminateInstances",param)
      #  print(result)
        return result

    def testDes(self):
        result=self.client.invoke("DescribeInstances",{})
     #   print(result)

