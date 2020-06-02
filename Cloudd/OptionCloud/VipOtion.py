import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import xmltodict,cloudutil

class VPCOption():
    def __init__(self,SubnetId,client):
        self.client=client
        self.SubnetID=SubnetId

    def CreateVip(self):
        # params={"SubnetId":self.SubnetID}
        params = {"SubnetId": self.SubnetID,"VipType":"KeepAlive"}
        CreateResult=self.client.invoke("CreateVip",params)
 #       print(CreateResult)
        try:
            CreateResultXmlResult = xmltodict.parse(CreateResult, encoding='utf-8')
            return CreateResultXmlResult["CreateVipResponse"]["CreateVipResult"]["vipId"]
        except Exception as e:
            return None


    def AddInstallVip(self,VipId,InstanceId):
        params={"VipId":VipId,"SubnetId":self.SubnetID,"InstanceId":InstanceId,"IsHeader":False}
        ADDresult=self.client.invoke("AddInstanceToVip",params)
        CreateResultXmlResult = xmltodict.parse(ADDresult, encoding='utf-8')
        return CreateResultXmlResult["AddInstanceToVipResponse"]["AddInstanceToVipResult"]["return"]

    def DescribeVips(self,VipId):
        params={"VipId":VipId,"SubnetId":self.SubnetID}
        DescribeResult=self.client.invoke("DescribeVips",params)
#        print(DescribeResult)
        DescribeResultXmlResult = xmltodict.parse(DescribeResult, encoding='utf-8')
        return DescribeResultXmlResult["DescribeVipsResponse"]["DescribeVipsResult"]["vipSet"]["item"]["privateIpAddress"]


if __name__=='__main__':
    VPC=VPCOption("subnet-6D6C0880")
    vpi=VPC.CreateVip()
    print(vpi)
    # print(VPC.DescribeVips(vpi))