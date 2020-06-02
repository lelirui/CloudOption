
import re
import subprocess,os
class ReadServiceScript():
    def __init__(self,ScriptName,ServiceObjectDict,ServiceList,log):
        self.ScriptName=ScriptName
        self.ServiceObjectDict=ServiceObjectDict
        self.ServiceList=ServiceList
        self.ScriptLineList=[]
        self.log=log


    def BasmRendScript(self,ServiceSriptPath):

        ScriptFileName=self.ScriptName+".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines() :
            self.ScriptLineList.append(ScriptFileLine)
        ScriptFile.close()
        self.log.info('Change Scirpt data')
        SSO=self.ServiceObjectDict['SipIp']
        if self.ServiceObjectDict['ServiceIMC'] == 'SDN':
            SdnAccesskeySub = subprocess.Popen('radosgw-admin user info --uid=bingo | grep -A1 access_key', shell=True,stdout=subprocess.PIPE)
            SdnAccesskeySub.wait()
            SdnAccesskey = SdnAccesskeySub.stdout.read()
            SdnAccesskey = str(SdnAccesskey, encoding="utf-8")
            SdnAccesskeyList = SdnAccesskey.split('"')
            SdnAccesskey=SdnAccesskeyList[3]
            SdnSecretkey=SdnAccesskeyList[7]

        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            if self.ServiceObjectDict['ServiceIMC'] == 'VAS':
                SSO=re.sub(r"\/script/","\/script/",self.ServiceObjectDict['SipIp'])
            if self.ServiceObjectDict['ServiceIMC'] == 'SDN':
                self.ScriptLineList[i] = re.sub(r"sdnAccessKey", SdnAccesskey, self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"sdnSecurityKey", SdnSecretkey, self.ScriptLineList[i])
            self.ScriptLineList[i]=re.sub(r"ssopoint", SSO,self.ScriptLineList[i])

    def SipRendScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptList=[]
        try:
            ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
            self.log.info('start read script ' + str(ScriptFileNamePath))
            ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
            self.log.info("Reading file .....")
            for ScriptFileLine in ScriptFile.readlines():
                self.ScriptLineList.append(ScriptFileLine)
            ScriptFile.close()
            self.log.info('Change Scirpt data')

            for i in range(len(self.ScriptLineList)):
                self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
                if self.ServiceObjectDict['ServiceNum']=='1':
                    self.ScriptLineList[i] = re.sub(r"db-master_ip", self.ServiceList[0]['InstanceIp'], self.ScriptLineList[i])
                else:

                    self.ScriptLineList[i] = re.sub(r"mysqlvip", self.ServiceList[-1], self.ScriptLineList[i])
                    self.ScriptLineList[i] = re.sub(r"db-master_ip", self.ServiceList[0]['InstanceIp'], self.ScriptLineList[i])
                    self.ScriptLineList[i] = re.sub(r"db-slave_ip", self.ServiceList[1]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"BCC_IP", self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1], self.ScriptLineList[i])
        except IOError as e:
            print("IoError ",e)
    


    def EcrReadScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()
        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')

            self.ScriptLineList[i] = re.sub(r"ecr_ip", self.ServiceList[0]['InstanceIp'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"sso_ip", self.ServiceObjectDict['SipIp'].split('/script/')[-2], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"cloudIp",  self.ServiceObjectDict['ServiceCloudIp'].split('/')[-1], self.ScriptLineList[i])

    def EcsReadScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()
        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            self.ScriptLineList[i] = re.sub(r"accesskey",self.ServiceObjectDict['ServiceAccessKey'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"securitykey", self.ServiceObjectDict['ServiceSecurityKey'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"endpoint", self.ServiceObjectDict['ServiceCloudIp'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"ssoIpaddr", self.ServiceObjectDict['SipIp'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"ecraddress", self.ServiceObjectDict['ServiceEcrIp'], self.ScriptLineList[i])

    def EksReadScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath=ServiceSriptPath+'/script/'+ScriptFileName
        self.log.info('start read script ' +str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')

        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()

        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            self.ScriptLineList[i] = re.sub(r"sso", self.ServiceObjectDict['SipIp'].split('/')[-2],self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"accessKey",self.ServiceObjectDict['ServiceAccessKey'], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"securitykey",  self.ServiceObjectDict['ServiceSecurityKey'], self.ScriptLineList[i])

    def SvzReadScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()

        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            self.ScriptLineList[i] = re.sub(r"SVZ_IP", self.ServiceList[0]["InstanceIp"], self.ScriptLineList[i])
            self.ScriptLineList[i] = re.sub(r"cloudpass",'pass@word1', self.ScriptLineList[i])

    def EFSReadScript(self, ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()

        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            self.ScriptLineList[i] = re.sub(r"vip", self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1], self.ScriptLineList[i])

    def CMPReadScript(self,ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/cmp/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()
        #servicelist 0: db 1:zabbix 2:ij 3:web
        self.log.info('Script num is '+str(len(self.ScriptLineList)))
        for i in range(len(self.ScriptLineList)):
            # self.log.info("Read default data is "+self.ScriptLineList[i])
            # self.log.info("Read ServiceNum is "+self.ServiceObjectDict['ServiceNum'])
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            if self.ServiceObjectDict['ServiceNum'] == '4':
                self.ScriptLineList[i] = re.sub(r"dbmaster_ip", self.ServiceList[0]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"webIp", self.ServiceList[-1]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"jobIp", self.ServiceList[-2]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"zabbixip", self.ServiceList[1]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"CPM_IJ", self.ServiceList[2]['InstanceIp'],
                                                self.ScriptLineList[i])
            elif self.ServiceObjectDict['ServiceNum'] == '8':
                self.ScriptLineList[i] = re.sub(r"mysqlvip", self.ServiceList[-1], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"dbmaster_ip", self.ServiceList[0]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"dbslave_ip", self.ServiceList[2]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"webIp", self.ServiceList[-2]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"sipserver_ip", self.ServiceList[1]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"j_ip", self.ServiceList[-3]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"inter_ip", self.ServiceList[-4]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"zabbixip", self.ServiceList[4]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"zabbixdbip", self.ServiceList[3]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"cmp_gateway", self.ServiceObjectDict['route'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"CPM_JOB", self.ServiceList[-3]['InstanceIp'],
                                                self.ScriptLineList[i])
            elif self.ServiceObjectDict['ServiceNum'] == '6':
                self.ScriptLineList[i] = re.sub(r"mysqlvip", self.ServiceList[-1], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"dbmaster_ip", self.ServiceList[0]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"dbslave_ip", self.ServiceList[1]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"webIp", self.ServiceList[-2]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"sipserver_ip", self.ServiceList[2]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"j_ip", self.ServiceList[-3]['InstanceIp'],
                                                self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"inter_ip", self.ServiceList[-4]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"monitorip", self.ServiceList[4]['InstanceIp'], self.ScriptLineList[i])
                self.ScriptLineList[i] = re.sub(r"cmp_gateway", self.ServiceObjectDict['route'],
                                                self.ScriptLineList[i])

            self.ScriptLineList[i] = re.sub(r"BCC_IP", self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1],
                                            self.ScriptLineList[i])

    def IAMReadScript(self, ServiceSriptPath):
        ScriptFileName = self.ScriptName + ".sh"
        ScriptFileNamePath = ServiceSriptPath + '/script/' + ScriptFileName
        self.log.info('start read script ' + str(ScriptFileNamePath))
        ScriptFile = open(str(ScriptFileNamePath), 'r', encoding='UTF-8')
        self.log.info("Reading file .....")

        for ScriptFileLine in ScriptFile.readlines():
            self.ScriptLineList.append(ScriptFileLine)
        self.log.info('Change Scirpt data')
        ScriptFile.close()
        # servicelist 0: db 1:zabbix 2:ij 3:web

        for i in range(len(self.ScriptLineList)):
            self.ScriptLineList[i] = self.ScriptLineList[i].strip('\n')
            self.ScriptLineList[i] = re.sub(r"localIp", self.ServiceList[0]['InstanceIp'],
                                            self.ScriptLineList[i])

    def HanderServiceToScript(self):
        ServiceSriptPath=os.getcwd()
        ServiceSriptPath='/opt/CloudOption/Cloudd'

        if re.search("ECR",self.ScriptName) is not None:
            self.EcrReadScript(ServiceSriptPath)
            return self.ScriptLineList
        elif re.search("ECS",self.ScriptName) is not None:
            self.EcsReadScript(ServiceSriptPath)
            return self.ScriptLineList
        elif re.search("CMP",self.ScriptName) is not None:
            self.CMPReadScript(ServiceSriptPath)
            return self.ScriptLineList    
        elif re.search("SIP",self.ScriptName) is not None:
            self.SipRendScript(ServiceSriptPath)

            return self.ScriptLineList
        elif re.search("EKS",self.ScriptName) is not None:
            self.EksReadScript(ServiceSriptPath)
            return self.ScriptLineList
        elif re.search("SVZ",self.ScriptName) is not None:
            self.SvzReadScript(ServiceSriptPath)
            return self.ScriptLineList
        elif re.search("EFS",self.ScriptName)is not None:
            self.EFSReadScript(ServiceSriptPath)
            return self.ScriptLineList
        elif re.search("IAM",self.ScriptName)is not None:
            self.IAMReadScript(ServiceSriptPath)
            return self.ScriptLineList
        else:
            self.BasmRendScript(ServiceSriptPath)
            return self.ScriptLineList
