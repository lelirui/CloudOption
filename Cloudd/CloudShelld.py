#!/bin/python3
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Cloudd'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
import socket
import json
import CloudThread
import subprocess
import LogOption


#json:{'option':'cancel',data:{service:{serviceimc:}}}
#{'option':'add',data:{service:{serviceimc:}}}

class CloudServerSock:
    SocketList = {}
    CloudThreadDict = {}
    def __init__(self):
        self.log=LogOption.LogOption()
        self.log.InitLog()

    def HandleSocker(self):
        self.log.info("Start CloudDaemon")
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 9999
        self.log.info('CloudDaemon bond 127.0.0.1:9999 success')
        self.serversocket.bind((host, port))
        self.serversocket.listen(10)
        self.log.info('CloudDaemon Waiting for someone else to connect')
        while True:
            clientsocket, addr = self.serversocket.accept()
            self.log.info(clientsocket)
            ClientJson = clientsocket.recv(2048)

            ClientJson = str(ClientJson, encoding="utf-8")
            ClientDateDict = json.loads(ClientJson)
            self.log.info("The data from the client is " + str(ClientDateDict))

            if ClientDateDict.get('Option') == 'cancel':
                if self.CloudThreadDict.get(ClientDateDict['ServiceIMC']) ==None:
                    pass
                else:
                    self.CloudThreadDict.get(ClientDateDict['ServiceIMC']).stop_thread()
                    self.CloudThreadDict.pop(ClientDateDict['ServiceIMC'])
                self.log.info(ClientDateDict['ServiceIMC']+' Stop is Success')

            else:
                CloudThreadService = CloudThread.Worker()
                CloudDict = {ClientDateDict['ServiceIMC']: CloudThreadService}
                self.CloudThreadDict.update(CloudDict)
                CloudSocketDict = {ClientDateDict['ServiceIMC']: clientsocket}
                self.SocketList.update(CloudSocketDict)
                CloudThreadService.Service(ClientDateDict, clientsocket, self.CloudThreadDict, self.GetCloudPassword(),self.log)
                CloudThreadService.start()

    def GetCloudPassword(self):
        CloudDBCfgSub = subprocess.Popen(
            ['cat', '/opt/bingocloud/latest/output/config/db.cfg'],
            stdout=subprocess.PIPE)
        CloudDBCfgSub.wait()
        CloudDBCat = CloudDBCfgSub.stdout.read()
        CloudDBCat = str(CloudDBCat, encoding="utf-8")
        CloudCatFileList = CloudDBCat.split('\n')
        return CloudCatFileList[-1].split(',')[-2].split('"')[1]


    def CloudThreadDictPop(self,ServiceIMC):
        self.CloudThreadDict.pop(ServiceIMC)

cloud=CloudServerSock()
cloud.HandleSocker()