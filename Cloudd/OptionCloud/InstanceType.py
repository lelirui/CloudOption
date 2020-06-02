import os,sys,re
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import xmltodict,cloudutil

class InstanceType():
    def __init__(self,client,log):
        self.client=client
        self.TypeName=['m1.micro','m1.medium','c1.micro','c1.small','c1.latge']
        self.log=log

    def InstanceTypeAll(self):
        result = self.client.invoke("DescribeInstanceTypes", {})
        InstanceTypeXmlList = xmltodict.parse(result, encoding='utf-8')
        return InstanceTypeXmlList["DescribeInstanceTypesResponse"]["instanceTypeInfo"]["item"]

    def HandleInstanceTypeAll(self,IsSip,IsCom):
        InstanceType=self.InstanceTypeAll()

        InstanceNameList=[]
        for i in range(len(InstanceType)):
            InstanceNameList.append(InstanceType[i]["instanceType"])
            if IsSip is True or IsCom == 5:
                if InstanceType[i]["cpu"] == '2' and InstanceType[i]["ram"] == '4096':
                    return InstanceType[i]["instanceType"]
            elif IsCom == 4:
                if InstanceType[i]["cpu"] == '4' and InstanceType[i]["ram"] == '16384':
                    return InstanceType[i]["instanceType"]
            elif InstanceType[i]["cpu"] == '4' and InstanceType[i]["ram"] == '8192':
                return InstanceType[i]["instanceType"]
        return InstanceNameList


    def HanderlCreateInstanceTyper(self,IsSip,IsCom=0):
        InstanceTyepName=self.HandleInstanceTypeAll(IsSip,IsCom)
        if isinstance(InstanceTyepName,str):
            return InstanceTyepName

        instanceTypeNamede = [l for l in InstanceTyepName if l in self.TypeName]
        instanceTypeNameChaji=[item for item in self.TypeName if item not in instanceTypeNamede]
        if IsSip==True or IsCom==5:
            self.CreateInstanceTypes(instanceTypeNameChaji[0],"2C4G",2,4096)
        elif IsCom == 4:
            self.CreateInstanceTypes(instanceTypeNameChaji[0], "4C16G", 4, 16384)
        else:
            self.CreateInstanceTypes(instanceTypeNameChaji[0], "4C8G", 4, 8192)
        return instanceTypeNameChaji[0]

    def CreateInstanceTypes(self,InTyName,InTyDisName,CpuNum,MemSize):
        params={'InstanceTypesName':InTyName,"InstanceTypesDisplayName":InTyDisName,"InstanceTypesCpu":CpuNum,
                "InstanceTypesMemory":MemSize,"InstanceTypesGpu":0,"InstanceTypesSsd":0,"InstanceTypesHdd":0,
                "InstanceTypesHba":0,"InstanceTypesSriov":0,'InstanceTypesIsBareMetal':False}
        result=self.client.invoke("CreateInstanceTypes",params)
        if re.search('Error',str(result)) is not None:
            resultlog='Failed to create a '+InTyDisName+' scale named '+InTyName
            self.log.info(str(result))
        else:
            resultlog = 'Success to create a ' + InTyDisName + ' scale named ' + InTyName
        self.log.info(resultlog)


#
#
# if __name__ == '__main__':
#
#     client=cloudutil.bcclient()
#     vpc_1 = InstanceType()
#     # vpc_1.InstanceTypeAll()
#     # vpc_1.CreateInstanceTypes("c1.large","4核8G",4,8)
#     result=vpc_1.HanderlCreateInstanceTyper(False,4)
#     print(result)
