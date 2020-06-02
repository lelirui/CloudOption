# import paramiko
# import os,sys,re
# sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
# from util import ReadServiceScript
# # import ReadServiceScript
# import time
# import nmap
# import threading
# from fabric.tasks import execute
# from fabric.api import *


# class CheckInstanceRun():
#     def __init__(self):
#         self.isCheck=False

#     def CheckIsRun(self,InstanceIp):
#         nm = nmap.PortScannerYield()
#         while True:
#             for result in nm.scan(InstanceIp, ports='22', arguments="-sV"):
#                 if result[-1]['nmap']['scanstats']['uphosts'] == '1':
#                     self.isCheck=True
#             if self.isCheck is True:
#                 break


# class InitServiceWorking(threading.Thread):
#     def ServiceInfo(self,ServiceList,ServiceObjectDict,log,ServiceNmaeList):
#         self.ServiceList = ServiceList
#         self.ServiceIMC = ServiceObjectDict['ServiceIMC']
#         self.ServiceObjectDict = ServiceObjectDict
#         self.ServiceNameList = ServiceNmaeList
#         self.log = log
#     def ServiceSort(self,num):
#         self.num=num
#     def run(self):
#         try:
#             if self.ServiceIMC == 'ECR' or self.ServiceIMC == 'SVZ' or self.ServiceIMC == 'ECR2' or self.ServiceIMC == 'EFS':
#                 if self.num == 0:
#                     result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[i]["InstanceIp"],self.num)
#                     if result != '0':
#                         return result
#                 else:
#                     self.TryConnect(self.ServiceList[0]["InstanceIp"])
#                     result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[0]["InstanceIp"])
                    
#                     if result != '0':
#                         return result
#             else:
#                 self.TryConnect(self.ServiceList[self.num]["InstanceIp"])
#                 result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[self.num]["InstanceIp"])
#                 if result != '0':
#                     return result
#         except Exception as e:
#             raise  e

#     def RunScriptInVM(self,serviceNames,ServiceIp,num=1):
#         self.log.info('Start reading scripts with instance name '+serviceNames)
#         readServiceScript=ReadServiceScript.ReadServiceScript(serviceNames,self.ServiceObjectDict,self.ServiceList,self.log)
#         self.ScriptList=readServiceScript.HanderServiceToScript()

#         if ServiceIp is '':
#             return None

    
#         if num == 0:
#             return execute(self.localFabfile)
#         else:
#             return execute(self.Long_rangeFabfile)
#         # for script in ScriptList:
            
#         #     if re.search("cmp_config_hosts_and_ntp.sh",script) is not None:
#         #         stdin.write('Y\n')
#         #         stdin.write(self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1]+'\n')

#     def localFabfile(self):
#         with settings(hide('everything'),warn_only=True):
#             for script in self.ScriptList:
#                 self.log.info('The script content is: [' +script+']')
#                 self.log.info('The script content is: [' +self.ServiceNameList[self.num]+'] and ip is ['+self.ServiceList[self.num]["InstanceIp"]+']')
#                 result=local(script)
#                 if int(result.return_code) > 0:
#                     self.log.error('The result of script execution is '+result)
#                     self.log.error( "'RunScriptException'")
#                     raise Exception("'RunScriptException'")
#                     break 
#                 else:
#                     self.log.info('The result of script execution is Success'+result)

#         self.log.info('The instance script is executed')
#         return '0'        

#     def Long_rangeFabfile(self):
#         with settings(hide('everything'),warn_only=True):
#             for script in self.ScriptList:
#                 self.log.info('The script content is: [' +script+']')
                # self.log.info('Executing host is: [' +self.ServiceNameList[self.num]+'] and ip is ['+self.ServiceList[self.num]["InstanceIp"]+']')

#                 result=run(script)
#                 #差一个输入ｎｔｐ地址
#                 self.log.info('The result of script execution is '+result)
#                 self.log.info('TScript execution status code ['+str(result.return_code)+']')

#         self.log.info('The instance script is executed')
#         return '0'
        
#     def TryConnect(self, ServiceIp, TryCount=0):
#         TrtCount = 0
#         if TryCount == 3:
#             return None
#         if TrtCount ==0 :
#             CheckInsyance=CheckInstanceRun()
#             CheckInsyance.CheckIsRun(ServiceIp)
#         env.hosts=[ServiceIp]
#         env.user='root'
#         paramiko.util.log_to_file('paramiko.log')
#         self.VmSSHConnect = paramiko.SSHClient()
#         self.VmSSHConnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#         passwordList = ["pass@word1", "pass@word2"]
#         for Passore in passwordList:
#             try:

#                 self.log.info('Start trying '+str(TrtCount))
#                 self.VmSSHConnect.connect(hostname=ServiceIp, username="root", password=Passore)
#                 self.VmSSHConnect.close()
#                 env.password=Passore
#                 break
#             except:
#                 if Passore != 'pass@word2':
#                     continue
#                 else:
#                     if TrtCount < 3:
#                         time.sleep(10)
#                         TryCount = TryCount + 1
#                         self.TryConnect(ServiceIp, TryCount)
#                     else:
#                         self.log.error('Failure to connect to an instance with IP as  ' + ServiceIp)
#                         self.log.error("'ConnectionException'")
#                         raise Exception("'ConnectionException'")

# class InitServiceScirpt():
#     def __init__(self,ServiceList,ServiceObjectDict,log):
#         self.ServiceList=ServiceList
#         self.ServiceIMC=ServiceObjectDict['ServiceIMC']
#         self.ServiceObjectDict=ServiceObjectDict
#         self.ServiceNameList = []
#         self.log=log

#     def HandlerService(self):
#         if self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'ECR1':
#             self.ServiceNameList.append("ECR_Cloud")
#             self.ServiceNameList.append(self.ServiceIMC)
#         elif self.ServiceIMC + self.ServiceObjectDict["ServiceNum"] == 'ECR21':
#             self.ServiceNameList.append("ECR_Cloud")
#             self.ServiceNameList.append(self.ServiceIMC)
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'ECS1':
#             self.ServiceNameList.append(self.ServiceIMC)
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SIP3':
#             self.ServiceNameList.append("SIP_Mysql_M")
#             self.ServiceNameList.append("SIP_Mysql_S")
#             self.ServiceNameList.append("SIP_Web")
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'EKS1':
#             self.ServiceNameList.append(self.ServiceIMC)
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SVZ1':
#             self.ServiceNameList.append('SVZ_Cloud')
#             self.ServiceNameList.append(self.ServiceIMC)
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SIP1':
#             self.ServiceNameList.append('SIP_WEB_MYSQL')
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'CMP4':
#             self.ServiceNameList.append('CMP_DB')
#             self.ServiceNameList.append('CMP_ZABBIX')
#             self.ServiceNameList.append('CMP_IJ')
#             self.ServiceNameList.append('CMP_WEB')
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'CMP8':
#             self.ServiceNameList.append('CMP_DB_Slave')
#             self.ServiceNameList.append('CMP_DB_MASTER')
#             self.ServiceNameList.append('CMP_SIP8')
#             self.ServiceNameList.append('CMP_ZabbixDB')
#             self.ServiceNameList.append('CMP_Zabbix_Web')
#             self.ServiceNameList.append('CMP_Interface')
#             self.ServiceNameList.append('CMP_Job')
#             self.ServiceNameList.append('CMP_WEB6')
#         elif self.ServiceIMC + self.ServiceObjectDict["ServiceNum"] == 'CMP6':
#             self.ServiceNameList.append('CMP_DB_Slave')
#             self.ServiceNameList.append('CMP_DB_MASTER')
#             self.ServiceNameList.append('CMP_SIP6')
#             self.ServiceNameList.append('CMP_Monitor')
#             self.ServiceNameList.append('CMP_IJ')
#             self.ServiceNameList.append('CMP_WEB')
#         elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'EFS1':
#             self.ServiceNameList.append("EFS_Cloud")
#             self.ServiceNameList.append(self.ServiceIMC)
#         else:
#             self.ServiceNameList.append(self.ServiceIMC)

#     def HandlerServiceListIp(self):
#         self.HandlerService()
#         NameListCount = len(self.ServiceNameList)
#         try:
#             if NameListCount > 3:
#                 Middle=NameListCount/2
#                 for i in range(0,NameListCount,2):

#                     ThreadingList=[]
#                     for j in range(i,i+2):
#                         InitWorking = InitServiceWorking()
#                         InitWorking.ServiceInfo(self.ServiceList, self.ServiceObjectDict, self.log,
#                                                 self.ServiceNameList)
#                         InitWorking.ServiceSort(j)
#                         ThreadingList.append(InitWorking)
#                     for ThreadWork in ThreadingList:
#                         ThreadWork.setDaemon(True)
#                         ThreadWork.start()
#                     for ThreadWork in ThreadingList:
#                         ThreadWork.join()


#             else:
#                 for i in range(NameListCount):
#                     InitWorking = InitServiceWorking()
#                     InitWorking.ServiceInfo(self.ServiceList, self.ServiceObjectDict, self.log, self.ServiceNameList)
#                     InitWorking.ServiceSort(i)
#                     InitWorking.start()
#                     InitWorking.join()
#         except Exception as e:
#             raise e
        # return '0'
import paramiko
import os,sys,re
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import ReadServiceScript
# import ReadServiceScript
import time
import nmap
import threading


class CheckInstanceRun():
    def __init__(self):
        self.isCheck=False

    def CheckIsRun(self,InstanceIp):
        nm = nmap.PortScannerYield()
        while True:
            for result in nm.scan(InstanceIp, ports='22', arguments="-sV"):
                if result[-1]['nmap']['scanstats']['uphosts'] == '1':
                    self.isCheck=True
            if self.isCheck is True:
                break


class InitServiceWorking(threading.Thread):
    def ServiceInfo(self,ServiceList,ServiceObjectDict,log,ServiceNmaeList):
        self.ServiceList = ServiceList
        self.ServiceIMC = ServiceObjectDict['ServiceIMC']
        self.ServiceObjectDict = ServiceObjectDict
        self.ServiceNameList = ServiceNmaeList
        self.log = log
    def ServiceSort(self,num):
        self.num=num
    def run(self):
        try:
            if self.ServiceIMC == 'ECR' or self.ServiceIMC == 'SVZ' or self.ServiceIMC == 'ECR2' or self.ServiceIMC == 'EFS':
                if self.num == 0:
                    self.TryConnect('127.0.0.1')
                    result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[i]["InstanceIp"])
                    self.CloseSSh()
                    if result != '0':
                        return result
                else:
                    self.TryConnect(self.ServiceList[0]["InstanceIp"])
                    result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[0]["InstanceIp"])
                    self.CloseSSh()
                    if result != '0':
                        return result
            else:
                self.TryConnect(self.ServiceList[self.num]["InstanceIp"])
                result = self.RunScriptInVM(self.ServiceNameList[self.num], self.ServiceList[self.num]["InstanceIp"])
                self.CloseSSh()
                if result != '0':
                    return result
        except Exception as e:
            raise  e

    def RunScriptInVM(self,serviceNames,ServiceIp):
        self.log.info('Start reading scripts with instance name '+serviceNames)
        readServiceScript=ReadServiceScript.ReadServiceScript(serviceNames,self.ServiceObjectDict,self.ServiceList,self.log)
        ScriptList=readServiceScript.HanderServiceToScript()

        if ServiceIp is '':
            return None
        for script in ScriptList:
            self.log.info('The script content is: [' +script+']')
            self.log.info('Executing host is: [' +serviceNames+'] and ip is ['+ServiceIp+']')

            stdin, stdout, stderr=self.VmSSHConnect.exec_command(script)
            if re.search("cmp_config_hosts_and_ntp.sh",script) is not None:
                stdin.write('Y\n')
                stdin.write(self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1]+'\n')
            # print(stderr.read().decode('utf-8'))

            ErrResult=stderr.read().decode('utf-8')

            if ErrResult is '':
                self.log.info('The result of script execution is '+ErrResult)
                continue
            else:
                self.log.error('The result of script execution is '+ErrResult)
                self.log.error( "'RunScriptException'")
                self.CloseSSh()
                try:
                    raise Exception("'RunScriptException'")
                except Exception as e:
                    raise Exception("'RunScriptException'")
                
        self.log.info('The instance script is executed')
        return '0'
    def TryConnect(self, ServiceIp, TryCount=0):
        self.log.info('Start trying to connect to an instance with IP as '+ServiceIp)
        TrtCount = 0
        if TryCount == 3:
            return None
        if TrtCount ==0 :
            CheckInsyance=CheckInstanceRun()
            CheckInsyance.CheckIsRun(ServiceIp)

        paramiko.util.log_to_file('paramiko.log')
        self.VmSSHConnect = paramiko.SSHClient()
        self.VmSSHConnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        passwordList = ["pass@word1", "pass@word2"]
        for Passore in passwordList:
            try:
                self.log.info('Start trying '+str(TrtCount))
                if ServiceIp == '127.0.0.1':
                    self.VmSSHConnect.connect(hostname=ServiceIp, username="root")
                    self.log.info('Successful connection to an instance with IP as '+ServiceIp)
                    break
                else:
                    self.VmSSHConnect.connect(hostname=ServiceIp, username="root", password=Passore)
                    self.log.info('Successful connection to an instance with IP as ' + ServiceIp)
                    break
            except:
                if Passore != 'pass@word2':
                    continue
                else:
                    if TrtCount < 3:
                        time.sleep(10)
                        TryCount = TryCount + 1
                        self.TryConnect(ServiceIp, TryCount)
                    else:
                        self.log.error('Failure to connect to an instance with IP as  ' + ServiceIp)
                        self.log.error("'ConnectionException'")
                        raise Exception("'ConnectionException'")

    def CloseSSh(self):
        self.VmSSHConnect.close()

class InitServiceScirpt():
    def __init__(self,ServiceList,ServiceObjectDict,log):
        self.ServiceList=ServiceList
        self.ServiceIMC=ServiceObjectDict['ServiceIMC']
        self.ServiceObjectDict=ServiceObjectDict
        self.ServiceNameList = []
        self.log=log

    def HandlerService(self):
        if self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'ECR1':
            self.ServiceNameList.append("ECR_Cloud")
            self.ServiceNameList.append(self.ServiceIMC)
        elif self.ServiceIMC + self.ServiceObjectDict["ServiceNum"] == 'ECR21':
            self.ServiceNameList.append("ECR_Cloud")
            self.ServiceNameList.append(self.ServiceIMC)
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'ECS1':
            self.ServiceNameList.append(self.ServiceIMC)
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SIP3':
            self.ServiceNameList.append("SIP_Mysql_M")
            self.ServiceNameList.append("SIP_Mysql_S")
            self.ServiceNameList.append("SIP_Web")
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'EKS1':
            self.ServiceNameList.append(self.ServiceIMC)
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SVZ1':
            self.ServiceNameList.append('SVZ_Cloud')
            self.ServiceNameList.append(self.ServiceIMC)
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'SIP1':
            self.ServiceNameList.append('SIP_WEB_MYSQL')
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'CMP4':
            self.ServiceNameList.append('CMP_DB')
            self.ServiceNameList.append('CMP_ZABBIX')
            self.ServiceNameList.append('CMP_IJ')
            self.ServiceNameList.append('CMP_WEB')
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'CMP8':
            self.ServiceNameList.append('CMP_DB_Slave')
            self.ServiceNameList.append('CMP_SIP8')
            self.ServiceNameList.append('CMP_DB_MASTER')
            self.ServiceNameList.append('CMP_ZabbixDB')
            self.ServiceNameList.append('CMP_Zabbix_Web')
            self.ServiceNameList.append('CMP_Interface')
            self.ServiceNameList.append('CMP_Job')
            self.ServiceNameList.append('CMP_WEB8')
        elif self.ServiceIMC + self.ServiceObjectDict["ServiceNum"] == 'CMP6':
            self.ServiceNameList.append('CMP_DB_Slave')
            self.ServiceNameList.append('CMP_DB_MASTER')
            self.ServiceNameList.append('CMP_SIP6')
            self.ServiceNameList.append('CMP_Monitor')
            self.ServiceNameList.append('CMP_IJ')
            self.ServiceNameList.append('CMP_WEB')
        elif self.ServiceIMC+self.ServiceObjectDict["ServiceNum"] == 'EFS1':
            self.ServiceNameList.append("EFS_Cloud")
            self.ServiceNameList.append(self.ServiceIMC)

        else:
            self.ServiceNameList.append(self.ServiceIMC)

        # print("self.ServiceNameList ",self.ServiceNameList)

    # def TryConnect(self, ServiceIp, TryCount=0):
    #     self.log.info('Start trying to connect to an instance with IP as '+ServiceIp)
    #     TrtCount = 0
    #     if TryCount == 3:
    #         return None
    #     if TrtCount ==0 :
    #         CheckInsyance=CheckInstanceRun()
    #         CheckInsyance.CheckIsRun(ServiceIp)
    #
    #     paramiko.util.log_to_file('paramiko.log')
    #     self.VmSSHConnect = paramiko.SSHClient()
    #     self.VmSSHConnect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #
    #     passwordList = ["pass@word1", "pass@word2"]
    #     for Passore in passwordList:
    #         try:
    #             self.log.info('Start trying '+str(TrtCount))
    #             if ServiceIp == '127.0.0.1':
    #                 self.VmSSHConnect.connect(hostname=ServiceIp, username="root")
    #                 self.log.info('Successful connection to an instance with IP as '+ServiceIp)
    #                 break
    #             else:
    #                 self.VmSSHConnect.connect(hostname=ServiceIp, username="root", password=Passore)
    #                 self.log.info('Successful connection to an instance with IP as ' + ServiceIp)
    #                 break
    #         except:
    #             if Passore != 'pass@word2':
    #                 continue
    #             else:
    #                 if TrtCount < 3:
    #                     time.sleep(10)
    #                     TryCount = TryCount + 1
    #                     self.TryConnect(ServiceIp, TryCount)
    #                 else:
    #                     self.log.error('Failure to connect to an instance with IP as  ' + ServiceIp)
    #                     self.log.error("'ConnectionException'")
    #                     raise Exception("'ConnectionException'")


    # def RunScriptInVM(self,serviceNames,ServiceIp):
    #     self.log.info('Start reading scripts with instance name '+serviceNames)
    #     readServiceScript=ReadServiceScript.ReadServiceScript(serviceNames,self.ServiceObjectDict,self.ServiceList,self.log)
    #     ScriptList=readServiceScript.HanderServiceToScript()
    #
    #     if ServiceIp is '':
    #         return None
    #     for script in ScriptList:
    #         self.log.info('The script content is: [' +script+']')
    #         stdin, stdout, stderr=self.VmSSHConnect.exec_command(script)
    #         if re.search("cmp_config_hosts_and_ntp.sh",script) is not None:
    #             stdin.write('Y\n')
    #             stdin.write(self.ServiceObjectDict['ServiceCloudIp'].split('//')[-1]+'\n')
    #         # print(stderr.read().decode('utf-8'))
    #
    #         ErrResult=stderr.read().decode('utf-8')
    #
    #         if ErrResult is '':
    #             self.log.info('The result of script execution is '+ErrResult)
    #             continue
    #         else:
    #             self.log.error('The result of script execution is '+ErrResult)
    #             self.log.error( "'RunScriptException'")
    #             self.CloseSSh()
    #             raise Exception("'RunScriptException'")
    #     self.log.info('The instance script is executed')
    #     return '0'
    #
    # def CloseSSh(self):
    #     self.VmSSHConnect.close()

    def HandlerServiceListIp(self):
        self.HandlerService()
        NameListCount = len(self.ServiceNameList)
        try:
            if NameListCount > 3:
                Middle=NameListCount//2
                for i in range(0,NameListCount,Middle):
                    if i==0:
                        h=Middle
                    else:
                        h=NameListCount
                    ThreadingList=[]
                    # for j in range(i,i+2):
                    for j in range(i,h):                        
                        InitWorking = InitServiceWorking()
                        InitWorking.ServiceInfo(self.ServiceList, self.ServiceObjectDict, self.log,
                                                self.ServiceNameList)
                        InitWorking.ServiceSort(j)
                        ThreadingList.append(InitWorking)
                    for ThreadWork in ThreadingList:
                        ThreadWork.setDaemon(True)
                        ThreadWork.start()
                    for ThreadWork in ThreadingList:
                        ThreadWork.join()


            else:
                for i in range(NameListCount):
                    InitWorking = InitServiceWorking()
                    InitWorking.ServiceInfo(self.ServiceList, self.ServiceObjectDict, self.log, self.ServiceNameList)
                    InitWorking.ServiceSort(i)
                    InitWorking.start()
                    InitWorking.join()
        except Exception as e:
            raise e
        #
        # for i in range(NameListCount):
        #     if self.ServiceIMC == 'ECR' or self.ServiceIMC == 'SVZ' or self.ServiceIMC == 'ECR2' or self.ServiceIMC == 'EFS':
        #         if i ==0:
        #             self.TryConnect('127.0.0.1')
        #             result = self.RunScriptInVM(self.ServiceNameList[i], self.ServiceList[i]["InstanceIp"])
        #             self.CloseSSh()
        #             if result != '0':
        #                 return result
        #         else:
        #             self.TryConnect(self.ServiceList[0]["InstanceIp"])
        #             result = self.RunScriptInVM(self.ServiceNameList[i], self.ServiceList[0]["InstanceIp"])
        #             self.CloseSSh()
        #             if result != '0':
        #                 return result
        #     else:
        #         self.TryConnect(self.ServiceList[i]["InstanceIp"])
        #         result = self.RunScriptInVM(self.ServiceNameList[i],self.ServiceList[i]["InstanceIp"])
        #         self.CloseSSh()
        #         if result != '0':
        #             return result
        return '0'

# data1={'ServiceIMC': 'SIP', 'ServiceName': '自助服务平台', 'ServiceDate': '2019-06-06 09:43:41', 'ServiceProcess': 0, 'ServiceIsInstall': 'false', 'ServiceStatus': '未安装', 'ServiceImage': 'ami-13006501', 'ServiceTempImage': 'null', 'ServiceIp': 'null', 'vpcid': 'vpc-ADDD7587', 'SipIp': '', 'ServiceNum': '1', 'subnetid': 'subnet-B7E812AB', 'id': 1, 'ServiceAccessKey': 'E1C75CEA9E6AD7CC5D67', 'ServiceSecurityKey': 'WzlGMTUwRTIwQkI0QTdBNEM1MTgyNTA3NUQ3OUMyMDEyRDVFQjg3QzJd', 'ServiceId': 1, 'ServiceSipIp': 'null', 'ServiceEcrIp': 'null', 'ServiceRootPassword': 'null', 'ServiceBingoPassword': 'null', 'ServiceIsUser': False, 'ServiceCloudIp': 'http://10.202.36.1', 'Option': 'install'}
# data2=[{'InstanceId': 'i-D93F9C58', 'InstanceIp': '10.202.36.100'}]
# init=InitServiceScirpt(data2,data1)
# init.HandlerServiceListIp()