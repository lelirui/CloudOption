import socket
import json
from datetime import datetime
from CloudApp import Images,CloudAppLog
from Cloudd.util import cloudutil


class CloudClient():
    def __init__(self):
        self.ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.log = CloudAppLog.CloudAppLog()
        self.log.InitLog()

    def HandleCloudService(self,ServiceObjectDict,ServiceIMC,ServiceImage,option):
        ServiceResultDateDict={}
        try:
            if self.CheckImage(ServiceImage) == True or option == 'cancel':
                self.ClientSocket.connect(('127.0.0.1', 9999))
                self.log.info('Connecting to the server')
                self.ClientSocket.send(bytes(ServiceObjectDict, encoding="utf8"))
                self.log.info('The data sent to the server is '+str(ServiceObjectDict))
                ServiceResultDateDict = {"ServiceIMC": ServiceIMC, 'ServiceResult': True,
                                         'ServiceOptionDate': str(datetime.now()),
                                         'ServiceOptionIsSuccess': 1}
        except ConnectionRefusedError as e:
            self.log.error("Failure to connect to server")
            ServiceResultDateDict = {"ServiceIMC": ServiceIMC, 'ServiceResult': False,
                               'ServiceOptionDate': str(datetime.now()),
                               'ServiceOptionIsSuccess': 0}

        finally:
            if len(ServiceResultDateDict)==0:
                ServiceResultDateDict = {"ServiceIMC": ServiceIMC, 'ServiceResult': False,
                                         'ServiceOptionDate': str(datetime.now()),
                                         'ServiceOptionIsSuccess': 0}
            self.log.info('Completion sent to the server')
            self.log.info('The server side returns data as '+str(ServiceResultDateDict))
            self.ClientSocket.close()

            return ServiceResultDateDict
    def CheckImage(self,ServiceImage):

        ImageObject=Images.instanceImage(cloudutil.bcclient())
        ImageIsExistence=ImageObject.get_image_id(ServiceImage)
        print("imagesid is ",ImageIsExistence)
        if ImageIsExistence is 'not':
            return False

        return True

#
# test=CloudClient()
# servicedict={'ServiceIMC': 'SIP', 'ServiceName': '自助服务平台', 'ServiceDate': '2019-06-06 09:43:41', 'ServiceProcess': 0, 'ServiceIsInstall': False, 'ServiceStatus': '安装中', 'ServiceImage': 'ami-13006503', 'ServiceTempImage': 'null', 'ServiceIp': None, 'vpcid': 'vpc-952183F6','subnetid':'subnet-728476A6', 'SipIp': '', 'ServiceNum': '1',"option":'install'}
# ServiceObejctJson=json.dumps(servicedict)
# test.HandleCloudService(ServiceObejctJson)
# test.HandleClose()