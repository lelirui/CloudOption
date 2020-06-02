import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from Cloudd.util import xmltodict,cloudutil


class vpc():
    def __init__(self):
        self.client = cloudutil.bcclient()

    def getAllVpc(self):
        params = {"Filter.1.Name": "cidr", "Filter.1.Value.1": "10.250.202.0/24"}
        result = self.client.invoke('DescribeVpcs', {})
        return result


    def getVpcAllsubnet(self,VPC_ID):
        params = {"Filter.1.Name": "vpc-id", "Filter.1.Value.1": VPC_ID}
        result = self.client.invoke('DescribeSubnets', params)

    def getALLXMLVpc(self):
        vpcxmlresult = xmltodict.parse(self.getAllVpc(), encoding='utf-8')
        try:
            vpcxmlresult=vpcxmlresult['DescribeVpcsResponse']['vpcSet']['item']
            return vpcxmlresult
        except Exception as e:
            return None

    def get_vpcid_subnet(self,vpcId):
        params = {"Filter.1.Name": "vpc-id", "Filter.1.Value.1": vpcId}
        subnetresult = self.client.invoke('DescribeSubnets', params)
        return  subnetresult

    def getXMLSubnet(self,vpcId):
        subnetresultxml = xmltodict.parse(self.get_vpcid_subnet(vpcId), encoding='utf-8')
        subnetresultxml = subnetresultxml['DescribeSubnetsResponse']['subnetSet']['item']
        return subnetresultxml




if __name__ == '__main__':

    client=cloudutil.bcclient()
    vpc_1 = vpc()
    print(vpc_1.getXMLSubnet())