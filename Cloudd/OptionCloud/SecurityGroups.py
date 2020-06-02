import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import xmltodict,cloudutil

class SecurityGroup():
    def __init__(self,client):
        self.client=client

    def CreateSevurityGroup(self,ServiceName):
        params={"GroupName":ServiceName}
        CreateResult=self.client.invoke("CreateSecurityGroup",params)
        CreateResultXmlResult = xmltodict.parse(CreateResult, encoding='utf-8')
        return CreateResultXmlResult["CreateSecurityGroupResponse"]["groupId"]

    #下行授权
    def AuthorizeSecurityGroupIngress(self,GroupId):
        params={"Policy":'ACCEPT',"IpProtocol":"ALL","FromPort":0,"ToPort":65535,"CidrIp":"0.0.0.0/0","GroupId":GroupId,
                "BoundType":"In","L2Accept":False}
        self.client.invoke("AuthorizeSecurityGroupIngress",params)



if __name__ == '__main__':

    client=cloudutil.bcclient()
    vpc_1 = SecurityGroup()

    # result=vpc_1.CreateSevurityGroup("teste")
    # print(result)
    vpc_1.AuthorizeSecurityGroupIngress("sg-A30CF59D")
