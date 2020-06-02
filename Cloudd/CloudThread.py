# coding=UTF-8
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'OptionClouds'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))

import string,random
import time,json
import pymysql
from datetime import datetime
import threading

import inspect
import ctypes
from OptionCloud import images
from util import cloudutil,InitServiceScript
from OptionCloud import InstanceType,Role,InstanceOption,Volume,VipOtion



class InstanceTypeConfig():
    def __init__(self,log):
        self.InstanceList=[]
        self.log=log
    def InstanceType(self,ServiceName,num,client):
        instanceType = InstanceType.InstanceType(client,self.log)
        if num == 1:
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict=({'ServiceName':ServiceName,'InstanceType':instanceTypeId})
            self.InstanceList.append(InstanceDict)

        elif num == 3:
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(True)
            InstanceDict = ({'ServiceName': ServiceName+'SlaverDB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            InstanceDict = ({'ServiceName': ServiceName+'MasterBD', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict = ({'ServiceName': ServiceName+'WEB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
        elif  num == 4:
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(True)
            InstanceDict = ({'ServiceName': ServiceName+'BD', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict = ({'ServiceName': ServiceName+'Zabbix', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False,num)
            InstanceDict = ({'ServiceName': ServiceName + 'Interface&job', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False,num)
            InstanceDict = ({'ServiceName': ServiceName + 'WEB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
        elif num == 6:
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False,4)
            InstanceDict = ({'ServiceName': ServiceName + 'BD-Slave', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False,4)
            InstanceDict = ({'ServiceName': ServiceName + 'BD-Master', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(True)
            InstanceDict = ({'ServiceName': ServiceName + 'Moniter-DB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'Interface&job', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'SipService', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'WEB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
        elif num == 8:
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'BD-Slave', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'SipService', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'BD-Master', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict = ({'ServiceName': ServiceName + 'Zabbix-DB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict = ({'ServiceName': ServiceName + 'Zabbix-Service', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False)
            InstanceDict = ({'ServiceName': ServiceName + 'Interface', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False,4)
            InstanceDict = ({'ServiceName': ServiceName + 'Job', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)
            
            instanceTypeId = instanceType.HanderlCreateInstanceTyper(False, 4)
            InstanceDict = ({'ServiceName': ServiceName + 'WEB', 'InstanceType': instanceTypeId})
            self.InstanceList.append(InstanceDict)

    def getInstanceTypeList(self):
        return self.InstanceList

class Worker(threading.Thread):
    
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working=True
        self.ServiceList=[]
        self.ServiceStep=None
        self.client=cloudutil.bcclient()
        self.Step='0'

    def stopThread(self):
        self.working=False

    def Service(self,ServiceObjectDict,ClientSocker,CloudThreadDict,CloudSqlPassword,log):
        self.ServiceObjectDict=ServiceObjectDict
        self.ClientSocker=ClientSocker
        self.CloudThreadDict=CloudThreadDict
        self.CloudSqlPassword=CloudSqlPassword
        self.log=log

    def Get_ServiceStepConfig(self):

        ServiceStepConfig={
            'EKS1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5,'name':'CreateVloment'},
                     'step3': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step4': {'Function': self.CloudServiceRegister, 'Weight': 4, 'name': 'RegisterService'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'VAS1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'SVZ1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'SIP3': {'step0': { 'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5,'name':'CreateVloment'},
                     'step3': {'Function': self.CreateVIP, 'Weight': 3,'name':'CreateVIP'},
                     'step4': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'SGW1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'SDN1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.CloudServiceRegister, 'Weight': 4,'name':'RegisterService'},
                     'step4': {'Function': self.FinishServiceInstance, 'Weight': 2,'name':'SuccessInstall'}},
            'NFV1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'EFS1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'ECS1': {'step0': {'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step3': {'Function': self.CloudServiceRegister, 'Weight': 4, 'name': 'RegisterService'},
                     'step4': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'ECR1': {'step0': { 'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5,'name':'CreateVloment'},
                     'step3': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step4': {'Function': self.CloudServiceRegister, 'Weight': 4, 'name': 'RegisterService'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessService'}},
            'ECR21': {'step0': {'Function': self.CheckImage, 'Weight': 4, 'name': 'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5, 'name': 'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5, 'name': 'CreateVloment'},
                     'step3': {'Function': self.InitInstance, 'Weight': 8, 'name': 'InitInitance'},
                     'step4': {'Function': self.CloudServiceRegister, 'Weight': 4, 'name': 'RegisterService'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessService'}},
            'CMP4': {'step0': { 'Function': self.CheckImage, 'Weight': 4,'name':'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5,'name':'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5,'name':'CreateVloment'},
                     'step3': {'Function': self.InitInstance, 'Weight': 8,'name':'InitInitance'},
                     'step4': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'CMP6': {'step0': {'Function': self.CheckImage, 'Weight': 4, 'name': 'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5, 'name': 'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5, 'name': 'CreateVloment'},
                     'step3': {'Function': self.CreateVIP, 'Weight': 3, 'name': 'CreateVIP'},
                     'step4': {'Function': self.InitInstance, 'Weight': 8, 'name': 'InitInitance'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'CMP8': {'step0': {'Function': self.CheckImage, 'Weight': 4, 'name': 'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5, 'name': 'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5, 'name': 'CreateVloment'},
                     'step3': {'Function': self.CreateVIP, 'Weight': 3, 'name': 'CreateVIP'},
                     'step4': {'Function': self.InitInstance, 'Weight': 8, 'name': 'InitInitance'},
                     'step5': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'SIP1': {'step0': {'Function': self.CheckImage, 'Weight': 4, 'name': 'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5, 'name': 'CreateInstance'},
                     'step2': {'Function': self.CreateVolent, 'Weight': 5, 'name': 'CreateVloment'},
                     'step3': {'Function': self.InitInstance, 'Weight': 8, 'name': 'InitInitance'},
                     'step4': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},
            'IAM1': {'step0': {'Function': self.CheckImage, 'Weight': 4, 'name': 'CheckImageExistence'},
                     'step1': {'Function': self.CreateInstance, 'Weight': 5, 'name': 'CreateInstance'},
                     'step2': {'Function': self.InitInstance, 'Weight': 8, 'name': 'InitInitance'},
                     'step3': {'Function': self.FinishServiceInstance, 'Weight': 2, 'name': 'SuccessInstall'}},

        }
        return ServiceStepConfig.get(self.ServiceObjectDict['ServiceIMC']+self.ServiceObjectDict['ServiceNum'])

    def run(self):
        try:
            ServiceStep = self.Get_ServiceStepConfig()
            self.log.info('Start installing '+self.ServiceObjectDict['ServiceIMC']+' services')
            ServiceStepCount=len(ServiceStep)
            WightCount=0
            self.log.info('The number of steps required to install '+self.ServiceObjectDict['ServiceIMC']+' is '+str(ServiceStepCount))
            for i in range(ServiceStepCount):
                self.Step = 'step' + str(i)
                WightCount=WightCount+ServiceStep[self.Step]['Weight']

            self.UpdateServiceLog('update CloudApp_service set ServiceStatus=null WHERE ServiceIMC="'+self.ServiceObjectDict["ServiceIMC"]+'"')
            SetpWeight=0
            for i  in range(ServiceStepCount):
                self.Step='step'+str(i)
                self.log.info('The steps being performed are '+self.Step)
                Function=ServiceStep[self.Step]['Function']
                result=Function()
                if result==True:
                    SetpWeight=SetpWeight+ServiceStep[self.Step]['Weight']
                    Percentage=SetpWeight/WightCount
                else:
                    self.log.error('The service '+self.ServiceObjectDict["ServiceIMC"]+' execution step '+ServiceStep[self.Step]['name']+' failed')
                    Percentage=0
                self.log.info('Service '+self.ServiceObjectDict["ServiceIMC"]+' percentage is '+str(Percentage*100))
                PercentageList=int(Percentage*100)
                self.UpdateServiceLog('update CloudApp_service set ServiceProcess=%s where ServiceIMC="' +self.ServiceObjectDict["ServiceIMC"] + '"',PercentageList)
                #self.WriteOptionLog(ServiceStep[self.Step]['name'],ServiceStep[self.Step]['name'],'1',self.ServiceObjectDict['ServiceIMC'])

        except Exception as e:
            Faile_f=e.__str__()
            self.log.error('exception occurred, The Exception is '+Faile_f)
            Faile=Faile_f.split("'")[1]
            self.log.error('Service install failed')
            self.log.error(Faile_f)
            self.UpdateServiceLog(
                'update CloudApp_service set ServiceProcess=%s where ServiceIMC="' + self.ServiceObjectDict[
                    "ServiceIMC"] + '"', 0)
            if Faile == 'RunInstancesResponse':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "创建实例失败，请检查配额/网络信息")
            elif Faile == 'CreateVolumeResponse':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "创建存储失败，请检查配额")
            elif Faile == 'AttachVolumeResponse':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "实例添加存储失败")
            elif Faile == 'AddInstanceToVipResponse':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "实例添加VIP失败")
            elif Faile == 'CreateVipResponse':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "创建vip失败")
            elif Faile == 'ConnectionException':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "连接实例失败，请查看安全组是否开放22端口")
                self.stop_thread()
            elif Faile ==  'RunScriptException' or Faile_f == 'RunScriptException':
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "脚本运行失败，请检查脚本")
                self.stop_thread()
            else:
                self.UpdateServiceLog(
                    'update CloudApp_service set ServiceOption=%s where ServiceIMC="' + self.ServiceObjectDict[
                        "ServiceIMC"] + '"', "脚本运行失败，请检查脚本")
                self.stop_thread()
            # self.WriteOptionLog('Mount Volume', Faile, '0',
            #                     self.ServiceObjectDict['ServiceIMC'])

        finally:
            self.CloudThreadDict.pop(self.ServiceObjectDict['ServiceIMC'])
            self.log.info('Service '+self.ServiceObjectDict['ServiceIMC']+' thread is end')

    def stop_thread(self):
        self.async_raise(self.ident, SystemExit)

    def async_raise(self, tid, exctype):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


    def CheckImage(self):
        self.log.info('Check Service '+self.ServiceObjectDict['ServiceIMC'] +' Image is exticence')

        ImageObject=images.instanceImage(self.client)
        ImageIsExistence=ImageObject.get_image_id(self.ServiceObjectDict['ServiceImage'])


        if ImageIsExistence is 'not':
            self.log.error('The mirror '+self.ServiceObjectDict['ServiceImage']+' of the service does not exist ')
         #   self.WriteOptionLog('Check Image', ImageOption, '0',self.ServiceObjectDict['ServiceIMC'])
            return False

        #self.WriteOptionLog('Check Image', ImageOption, '1',self.ServiceObjectDict['ServiceIMC'])
        self.log.info('The mirror '+self.ServiceObjectDict['ServiceImage']+' of the service exists ')

        return True

    def CreateInstance(self):
        role = Role.Role(self.client)
        ServiceNum=1
        instanceType=InstanceTypeConfig(self.log)
        self.log.info('Successful role creation for '+self.ServiceObjectDict['ServiceIMC'])
        if self.ServiceObjectDict['ServiceIMC'] == 'SDN':
            roleName = role.CreateRole("sdnvops")
            role.RoleModPower("sdnvops")
        else:
            roleName = role.CreateRole(self.ServiceObjectDict['ServiceIMC'].lower())
            role.RoleModPower(self.ServiceObjectDict['ServiceIMC'].lower())


        RoleOpttion='Create Role '+self.ServiceObjectDict['ServiceIMC'].lower() +' and RoleID is '+roleName+' Successfully'
        self.log.info(RoleOpttion)
        # self.WriteOptionLog('Create Role', RoleOpttion, '1',
        #                     self.ServiceObjectDict['ServiceIMC'])

        if self.ServiceObjectDict['ServiceIMC'] == 'SIP' or self.ServiceObjectDict['ServiceIMC'] == 'CMP' or self.ServiceObjectDict['ServiceIMC'] == '':
            if self.ServiceObjectDict['ServiceNum'] == '3':
                ServiceNum = 3
            elif self.ServiceObjectDict['ServiceNum'] == '4':
                ServiceNum = 4
            elif self.ServiceObjectDict['ServiceNum'] == '8':
                ServiceNum = 8
            elif self.ServiceObjectDict['ServiceNum'] == '6':
                ServiceNum = 6
        self.log.info('Start creating instance types')
        instanceType.InstanceType(self.ServiceObjectDict['ServiceIMC'],ServiceNum,self.client)
        InstanceList=instanceType.getInstanceTypeList()
        for instanceListType in InstanceList:
            instanceTypeOption='Init Instancetype '+instanceListType['InstanceType']+' is Successfully'
            self.log.info(instanceTypeOption)
        # self.WriteOptionLog('Init Instancetype', instanceTypeOption, '1',
        #                     self.ServiceObjectDict['ServiceIMC'])
        for i in range(ServiceNum):
            ServiceDict={}
            self.log.info('Start to create platform '+str(i+1)+' instance')
            instance = InstanceOption.InstanceOption(self.client)
            instanceId = instance.getCreateInstanceID(self.ServiceObjectDict['ServiceImage'], InstanceList[i]['InstanceType'],
                                                       self.ServiceObjectDict['vpcid'], self.ServiceObjectDict['subnetid'],
                                                      InstanceList[i]['ServiceName'], 50,roleName, "")
            ServiceDict.update({'InstanceId':instanceId})
            time.sleep(20)
            instanceIp = instance.InstanceXMLIpInfo(self.ServiceObjectDict['vpcid'],instanceId)
            ServiceDict.update({'InstanceIp':instanceIp})
            self.ServiceList.append(ServiceDict)
            InstanceOptionLog='Create '+InstanceList[i]['ServiceName']+' an instance ID for '+instanceId+' and  instance IP for '+instanceIp+' successfully'
            self.log.info(InstanceOptionLog)
            # self.WriteOptionLog('Create Instance', InstanceOptionLog, '1',
            #                     self.ServiceObjectDict['ServiceIMC'])
        self.log.info('ServiceList is length '+str(len(self.ServiceList)))
        return True

    def CreateVolent(self):
        VolumeSizeDict = {'SIP': '120', 'CMP': '200', 'ECR':'1024','EKS':'50','ECR2':'200'}
        VolumeOption = Volume.VolumeOption(self.client)
        self.log.info('Start creating storage '+VolumeSizeDict[self.ServiceObjectDict['ServiceIMC']]+'G for '+self.ServiceObjectDict['ServiceIMC']+' services')
        for i in range(len(self.ServiceList)):
            VolumeID = VolumeOption.CreateVolume(self.ServiceObjectDict['ServiceIMC'],VolumeSizeDict[self.ServiceObjectDict['ServiceIMC']])
            self.log.info('The storage of instance '+self.ServiceList[i]['InstanceId']+' was successfully created with the storage ID '+VolumeID)
            self.log.info('The /dev/sdb stored as an instance')
            time.sleep(7)
            VolumeOption.Instance_Vloume(self.ServiceList[i]['InstanceId'], VolumeID)
            self.log.info('Instance ' + self.ServiceList[i]['InstanceId'] + ' storage hangs successfully')

            if self.ServiceObjectDict['ServiceIMC'] == 'SIP' and self.ServiceObjectDict['ServiceNum'] == '1':
                VolumeID = VolumeOption.CreateVolume(self.ServiceObjectDict['ServiceIMC'],
                                                     VolumeSizeDict[self.ServiceObjectDict['ServiceIMC']])
                self.log.info('The storage of instance ' + self.ServiceList[i][
                    'InstanceId'] + ' was successfully created with the storage ID ' + VolumeID)
                self.log.info('The /dev/sdc stored as an instance')
                time.sleep(7)
                VolumeOption.Instance_Vloume(self.ServiceList[i]['InstanceId'], VolumeID, '/dev/vdc')
                self.log.info('Instance ' + self.ServiceList[i]['InstanceId'] + ' storage hangs successfully')
            if self.ServiceObjectDict['ServiceIMC'] == 'CMP' and i == len(self.ServiceList)-1:
                VolumeID = VolumeOption.CreateVolume(self.ServiceObjectDict['ServiceIMC'],
                                                     VolumeSizeDict[self.ServiceObjectDict['ServiceIMC']])
                self.log.info('The storage of instance ' + self.ServiceList[i][
                    'InstanceId'] + ' was successfully created with the storage ID ' + VolumeID)
                self.log.info('The /dev/sdc stored as an instance')
                time.sleep(7)
                VolumeOption.Instance_Vloume(self.ServiceList[i]['InstanceId'], VolumeID, '/dev/vdc')
                self.log.info('Instance ' + self.ServiceList[i]['InstanceId'] + ' storage hangs successfully')

            VolumeOptionLog='Success in creating storage and mounting '+self.ServiceObjectDict['ServiceIMC']+' instances'
            self.log.info(VolumeOptionLog)
        return True

    def CreateVIP(self):
        self.log.info('Start creating virtual Ip for '+self.ServiceObjectDict['ServiceIMC']+' services')
        if self.ServiceObjectDict['ServiceNum'] == '1':
            self.ServiceList.append(None)

        VipOptionObject = VipOtion.VPCOption(self.ServiceObjectDict['subnetid'],self.client)
        VipId = VipOptionObject.CreateVip()
        if VipId is None:
            return None
        AddResult = VipOptionObject.AddInstallVip(VipId, self.ServiceList[0]['InstanceId'])
        if AddResult is False:
            return None
        if self.ServiceObjectDict['ServiceIMC']  == 'CMP' and self.ServiceObjectDict['ServiceNum'] == '8':
            AddResult = VipOptionObject.AddInstallVip(VipId, self.ServiceList[2]['InstanceId'])
        else:
            AddResult = VipOptionObject.AddInstallVip(VipId, self.ServiceList[1]['InstanceId'])
        if AddResult is False:
            return None
        self.ServiceList.append(VipOptionObject.DescribeVips(VipId))
        VipOtionLog='Successful addition of VIP '+VipOptionObject.DescribeVips(VipId)+'for instances '+self.ServiceList[0]['InstanceId']+' instance and '+self.ServiceList[1]['InstanceId']+'in the Serivce'+self.ServiceObjectDict['ServiceIMC']
        self.log.info(VipOtionLog)
        # self.WriteOptionLog('Mount VIP', VipOtionLog, '1',
        #                     self.ServiceObjectDict['ServiceIMC'])

        return True

    def InitInstance(self):


        self.log.info('Start initializing an instance of service '+self.ServiceObjectDict['ServiceIMC'])
        # print(self.ServiceList)
        InitRunInstance=InitServiceScript.InitServiceScirpt(self.ServiceList,self.ServiceObjectDict,self.log)
        InitRunInstance.HandlerServiceListIp()
        self.log.info('Instance initialization of service '+self.ServiceObjectDict['ServiceIMC']+' is completed')
        return True


    # def WriteOptionLog(self,OptionName,OptionActive,IsSuccess,ServiceMIC):
    #
    #     CloudSqlDB = pymysql.connect('localhost', 'bingocloud', self.CloudSqlPassword, 'CloudOption', charset='utf8')
    #     CloudCursor = CloudSqlDB.cursor()
    #     NowTime=datetime.now()
    #     try:
    #         AddLogSql='insert into CloudApp_servicelog (ServiceOptionDate,ServiceOptionName,ServiceOption,ServiceIMC_id,ServiceOptionIsSuccess)'\
    #                   ' values("'+str(NowTime) +'","'+OptionName+'","'+OptionActive+'","'+ServiceMIC+'",'+IsSuccess+')'
    #
    #         CloudCursor.execute(AddLogSql)
    #         CloudSqlDB.commit()
    #     except:
    #         CloudSqlDB.rollback()
    #     finally:
    #         CloudCursor.close()
    #         CloudSqlDB.close()

    def UpdateServiceLog(self,optionSql,OptionData=0):
        CloudSqlDB = pymysql.connect('localhost', 'bingocloud', self.CloudSqlPassword, 'CloudOption', charset='utf8')
        CloudCursor = CloudSqlDB.cursor()

        try:
            if OptionData==0:
                CloudCursor.execute(optionSql)
            else:

                CloudCursor.execute(optionSql,OptionData)
            CloudSqlDB.commit()
        except:
            CloudSqlDB.rollback()
        finally:
            CloudCursor.close()
            CloudSqlDB.close()

    def CloudServiceRegister(self):
        self.log.info('Start registering service '+self.ServiceObjectDict['ServiceIMC'] +' to cloud platform')
        CloudSqlDB = pymysql.connect('localhost', 'bingocloud', self.CloudSqlPassword, 'bingocloud', charset='utf8')
        CloudCursor = CloudSqlDB.cursor()
        NowTime = datetime.now()
        RegiestTime=str(NowTime).split('.')[0]
        try:
            if self.ServiceObjectDict['ServiceIMC'] == 'ECR':
                if CloudCursor.execute('select * from serviceinfo where serviceCode="ECR"') == 1:
                    RegiestSql ='update serviceinfo set apiAddress="http://'+self.ServiceList[0].get("InstanceIp")+':10001/ecr/api",mgrAddress="http://'+self.ServiceList[0].get('InstanceIp')+':8079/manage",uiAddress="http://'+self.ServiceList[0].get('InstanceIp')+':10001" where serviceCode="ecr"'
                else:
                    RegiestSql = 'INSERT INTO serviceinfo VALUES ("srv-'+self.GetRandomString()+'", "容器镜像仓库服务", "ecr", "", "http://'+self.ServiceList[0].get("InstanceIp")+':10001/ecr/api", "http://'+self.ServiceList[0].get('InstanceIp')+':8079/manage", "http://'+self.ServiceList[0].get('InstanceIp')+':10001", NULL, "starting", "bingo","'+RegiestTime+'" , "'+RegiestTime+'", NULL, NULL, "'+RegiestTime+'", "failed", NULL, "noaction", "delete", 93, "advanced", 0, "outer", NULL, "node", NULL, NULL, NULL)'
            elif self.ServiceObjectDict['ServiceIMC'] == 'ECR2':
                if CloudCursor.execute('select * from serviceinfo where serviceCode="ECR"') == 1:
                    RegiestSql = 'update serviceinfo set apiAddress="http://' + self.ServiceList[0].get(
                        "InstanceIp") + '/api",mgrAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + '",uiAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + '" where serviceCode="ecr"'
                else:
                    RegiestSql = 'INSERT INTO serviceinfo VALUES ("srv-' + self.GetRandomString() + '", "容器镜像仓库服务", "ecr", "", "http://' + \
                                 self.ServiceList[0].get("InstanceIp") + 'api", "http://' + self.ServiceList[
                                     0].get('InstanceIp') + '", "http://' + self.ServiceList[0].get(
                        'InstanceIp') + '", NULL, "starting", "bingo","' + RegiestTime + '" , "' + RegiestTime + '", NULL, NULL, "' + RegiestTime + '", "failed", NULL, "noaction", "delete", 93, "advanced", 0, "outer", NULL, "node", NULL, NULL, NULL)'


            elif self.ServiceObjectDict['ServiceIMC'] == 'ECS':
                RegiestSql = 'update serviceInfo set uiAddress="http://'+self.ServiceList[0].get('InstanceIp')+':10000",status="started",registerAccount="bingo",registerTime="'+RegiestTime+'",starttime="'+RegiestTime+'",cloudService="outer" where serviceCode="ecs"'
            elif self.ServiceObjectDict['ServiceIMC'] == 'EKS':
                if CloudCursor.execute('select * from serviceinfo where serviceCode="eks"') == 1:
                    RegiestSql = 'update serviceinfo set apiAddress="http://' + self.ServiceList[0].get(
                        "InstanceIp") + ':8000/api",mgrAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + ':8000",uiAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + ':8000" where serviceCode="ecr"'

                else:
                    RegiestSql = 'INSERT INTO serviceinfo VALUES ("srv-' + self.GetRandomString() + '", "EKS容器服务", "eks", "", "http://' + \
                             self.ServiceList[0].get("InstanceIp") + ':8000/api", "http://' + self.ServiceList[
                                 0].get('InstanceIp') + ':8000", "http://' + self.ServiceList[0].get(
                    'InstanceIp') + ':8000", NULL, "starting", "bingo","'+RegiestTime+'" , "'+RegiestTime+'", NULL, NULL, "'+RegiestTime+'", "failed", NULL, "noaction", "delete", 94, "advanced", 0, "outer", NULL, "node", NULL, NULL, NULL)'
            elif  self.ServiceObjectDict['ServiceIMC'] == 'SDN':
                if CloudCursor.execute('select * from serviceinfo where serviceCode="sdnvops"') == 1:
                    RegiestSql = 'update serviceinfo set apiAddress="http://' + self.ServiceList[0].get(
                        "InstanceIp") + ':8079/manage ",mgrAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + ':8080",uiAddress="http://' + self.ServiceList[0].get(
                        'InstanceIp') + ':8080" where serviceCode="sdnvops"'

                else:
                    RegiestSql = 'INSERT INTO serviceinfo VALUES ("srv-' + self.GetRandomString() + '", "SDN可视化", "sdnvops", "", "http://' + \
                             self.ServiceList[0].get("InstanceIp") + ':8080 ", "http://' + self.ServiceList[
                                 0].get('InstanceIp') + ':8079/manage", "http://' + self.ServiceList[0].get(
                    'InstanceIp') + ':8080", NULL, "started", "bingo","'+RegiestTime+'" , "'+RegiestTime+'", NULL, NULL, "'+RegiestTime+'", "failed", NULL, "noaction", "delete", 96, "advanced", 0, "outer", NULL, "node", NULL, NULL, NULL)'
            self.log.info(RegiestSql)

            CloudCursor.execute(RegiestSql)
            CloudSqlDB.commit()
            self.log.info('Service '+self.ServiceObjectDict['ServiceIMC'] +' successfully registered to cloud platform')
        except:
            CloudSqlDB.rollback()
            self.log.info('Failure to register service '+self.ServiceObjectDict['ServiceIMC'] +' to cloud platform')

        finally:
            CloudCursor.close()
            CloudSqlDB.close()

        return True

    def GetRandomString(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=41))

    def FinishServiceInstance(self):
        ServiceName=self.ServiceObjectDict['ServiceIMC']+self.ServiceObjectDict['ServiceNum']
        if ServiceName == 'SIP3':
            self.UpdateServiceLog(
                'update CloudApp_service set ServiceProcess=100 ,ServiceIsInstall=1 ,ServiceStatus= 1 ,ServiceIp="' +
                self.ServiceList[2].get("InstanceIp") + '" ,ServiceDate="'+str(datetime.now())+'" where ServiceIMC="' +
                self.ServiceObjectDict["ServiceIMC"] + '"')
            self.UpdateServiceLog('update CloudApp_serviceconfig set ServiceSipIp=http://"' + self.ServiceList[2].get(
                "InstanceIp") + '/sso" where ServiceId=0')
        elif ServiceName == 'ECR':
            self.UpdateServiceLog(
                'update CloudApp_service set ServiceProcess=100,ServiceIsInstall=1 ,ServiceStatus= 1 ,ServiceIp="' +
                self.ServiceList[0].get("InstanceIp") + '" ,ServiceDate="'+str(datetime.now())+'" where ServiceIMC="' +
                self.ServiceObjectDict["ServiceIMC"] + '"')
            self.UpdateServiceLog('update CloudApp_serviceconfig set ServiceEcrIp="'+self.ServiceList[0].get("InstanceIp")+'" where ServiceId=0')
        elif ServiceName == 'CMP':
            self.UpdateServiceLog(
                'update CloudApp_service set ServiceProcess=100 ,ServiceIsInstall=1 ,ServiceStatus= 1 ,ServiceIp="' +
                self.ServiceList[-1].get("InstanceIp") + '" ,ServiceDate="' + str(
                    datetime.now()) + '" where ServiceIMC="' +
                self.ServiceObjectDict["ServiceIMC"] + '"')
            self.UpdateServiceLog('update CloudApp_serviceconfig set ServiceSipIp=http://"' + self.ServiceList[-1].get(
                "InstanceIp") + '/sso" where ServiceId=0')
        else:
            self.UpdateServiceLog(
                'update CloudApp_service set ServiceProcess=100,ServiceIsInstall=1 ,ServiceStatus= 1 ,ServiceIp="' +
                self.ServiceList[0].get("InstanceIp") + '" ,ServiceDate="'+str(datetime.now())+'" where ServiceIMC="' +
                self.ServiceObjectDict["ServiceIMC"] + '"')
            self.UpdateServiceLog('update CloudApp_serviceconfig set ServiceSipIp=http://"' + self.ServiceList[0].get(
                "InstanceIp") + '/sso" where ServiceId=0')
        self.log.info('Service '+self.ServiceObjectDict['ServiceIMC']+' installation completed')
        return True