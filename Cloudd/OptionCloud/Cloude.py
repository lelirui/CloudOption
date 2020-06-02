import sys,os,base64
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))

import xmltodict


class ClodeInfo():
    def __init__(self,client):
        self.client=client

    def getCloudeInfo(self):
        result = self.client.invoke("DescribeCloud", {})
        print(result)

    def getClusterInfo(self):
        result = self.client.invoke("DescribeClusters", {})
        return xmltodict.parse(result, encoding='utf-8')

    def getClusterName(self):
        ClusterInfo=self.getClusterInfo()
        ClusterInfo=ClusterInfo['DescribeClustersResponse']['clusterSet']['item']
        if len(ClusterInfo) < 9 and len(ClusterInfo) >1:
            return ClusterInfo[0]['clusterId']
        return ClusterInfo['clusterId']

