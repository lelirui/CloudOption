from django.shortcuts import render
from CloudApp.models import Authentication,Service,ServiceDisk,ServiceConfig
from CloudApp import CloudClient,CloudDisk,CloudDiskNum

# Create your views here.
from django.http import HttpResponse
import json

from django.forms.models import model_to_dict
from Cloudd.OptionCloud import vpc
from Cloudd.util import cloudutil
from datetime import datetime
import random,string
def AuthenticationView(request):
    PostBody=request.body.decode('UTF-8')
    json_result = json.loads(PostBody)
    AccessKey=json_result.get('username')
    SecurityKey=json_result.get('password')

    try:
        Auths=Authentication.objects.get(ServiceAccessKey=AccessKey)
        if Auths.ServiceSecurityKey == SecurityKey:
            ServiceTokenTime=Auths.ServiceTokenTime
            ServiceTokenTime=ServiceTokenTime.strftime('%Y-%m-%d %H:%M:%S')
            ServiceTokenTimeList=ServiceTokenTime.split(' ')
            ServiceTokenTime=datetime(int(ServiceTokenTimeList[0].split('-')[0]),int(ServiceTokenTimeList[0].split('-')[1]),int(ServiceTokenTimeList[0].split('-')[-1]),int(ServiceTokenTimeList[-1].split(':')[0]),int(ServiceTokenTimeList[-1].split(':')[1]),int(ServiceTokenTimeList[-1].split(':')[-1]),000000)
            NowTime=datetime.now()
            TokenTimeDiff=NowTime-ServiceTokenTime
            TokenTimeDiffInt=TokenTimeDiff.total_seconds()
            if TokenTimeDiffInt > 600:
                TokenString=''.join(random.choices(string.hexdigits, k=19))
                Auths.ServiceToken=TokenString
                Auths.ServiceTokenTime=datetime.now()
                Auths.save()
            else:
                TokenString=Auths.ServiceToken

            LoginResgist={"code":20000,"data":{"token":TokenString}}
        else:
            LoginResgist = {"code": 40400, "data": {"token": ""}}
    except Exception as e:

        LoginResgist={"code":40400,"data":{"token":""}}
    finally:

        StringJson=json.dumps(LoginResgist)
        return HttpResponse(StringJson)

def AuthenticationViewInfo(request):
    PostBody = request.body.decode('UTF-8')
    token=PostBody
    Auths = Authentication.objects.all()[0]
    ServiceTokenTime = Auths.ServiceTokenTime
    ServiceTokenTime = ServiceTokenTime.strftime('%Y-%m-%d %H:%M:%S')
    ServiceTokenTimeList = ServiceTokenTime.split(' ')
    ServiceTokenTime = datetime(int(ServiceTokenTimeList[0].split('-')[0]), int(ServiceTokenTimeList[0].split('-')[1]),
                                int(ServiceTokenTimeList[0].split('-')[-1]),
                                int(ServiceTokenTimeList[-1].split(':')[0]),
                                int(ServiceTokenTimeList[-1].split(':')[1]),
                                int(ServiceTokenTimeList[-1].split(':')[-1]), 000000)
    NowTime = datetime.now()
    TokenTimeDiff = NowTime - ServiceTokenTime
    TokenTimeDiffInt = TokenTimeDiff.total_seconds()
    if TokenTimeDiffInt < 1200:
        if Auths.ServiceToken == token:
            TokenString={"code": 20000,"data":{'roles': ['admin'],'introduction': 'I am a super administrator','avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'}}
        else:
            TokenString = {"code": 44400, "data": {'roles': ['admin'], 'introduction': 'I am a super administrator',
                                                   'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                                                   'name': 'Super Admin'}}
    else:
        TokenString = {"code": 44400, "data": {'roles': ['admin'], 'introduction': 'I am a super administrator',
                                               'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                                               'name': 'Super Admin'}}
    TokenAuthPerssion=json.dumps(TokenString)
    return HttpResponse(TokenAuthPerssion)




def ServiceList(request):

    ServiceList=Service.objects.all();
    ServiceListDict=[]
    for ServiceObject in ServiceList:
        ServiceObject.ServiceDate=ServiceObject.ServiceDate.strftime("%Y-%m-%d %H:%M:%S")
        if ServiceObject.ServiceStatus is False:
            ServiceObject.ServiceStatus='未安装'
        elif ServiceObject.ServiceStatus is True:
            ServiceObject.ServiceStatus='已安装'
        else:
            ServiceObject.ServiceStatus='安装中'
        ServiceObjectDict=model_to_dict(ServiceObject)

        ServiceListDict.append(ServiceObjectDict)
    ServiceDict={"code":20000,"data":{"total":10,'items':ServiceListDict}}
    ServiceJson=json.dumps(ServiceDict,ensure_ascii=False)
    return HttpResponse(ServiceJson)



def ServiceUpdate(request):
    # PostBody = request.body.decode('UTF-8')
    # json_result = json.loads(PostBody)
    # print(json_result)
    # return HttpResponse('test')
    while True:
        return HttpResponse('test')

def ServiceUpdateProcess(request):
    ServiceList = Service.objects.all();
    ServiceListDict = []
    for ServiceObject in ServiceList:
        if ServiceObject.ServiceStatus == 0:
            continue
        else:
            ServiceObject.ServiceDate = ServiceObject.ServiceDate.strftime("%Y-%m-%d %H:%M:%S")
            if ServiceObject.ServiceStatus is False:
                ServiceObject.ServiceStatus = '未安装'
            elif ServiceObject.ServiceStatus is True:
                ServiceObject.ServiceStatus = '已安装'
            else:
                ServiceObject.ServiceStatus = '安装中'
            ServiceObjectDict = model_to_dict(ServiceObject)

        ServiceListDict.append(ServiceObjectDict)
    ServiceDict = {"code": 20000, "data": {"total": 10, 'items': ServiceListDict}}
    ServiceJson = json.dumps(ServiceDict, ensure_ascii=False)
    return HttpResponse(ServiceJson)

def ServiceDel(request):
    PostBody = request.body.decode('UTF-8')
    ServiceDict = json.loads(PostBody)
    ServiceObject=Service.objects.get(ServiceIMC=ServiceDict['ServiceIMC'])
    ServiceObject.ServiceDate=str(datetime.now())
    ServiceObject.ServiceProcess=0
    ServiceObject.ServiceIsInstall=0
    ServiceObject.ServiceStatus=0
    ServiceObject.ServiceIp='null'
    ServiceObject.save()
    if ServiceDict['ServiceIMC'] == 'SIP':
        ServiceConfigObject = ServiceConfig.objects.all()[0]
        ServiceConfigObject.ServiceIsUser = 1
        ServiceConfigObject.ServiceSipIp='null'
        ServiceConfigObject.save()
    elif ServiceDict['ServiceIMC']=='ECR':
        ServiceConfigObject=ServiceConfig.objects.all()[0]
        ServiceConfigObject.ServiceIsUser=1
        ServiceConfigObject.ServiceEcrIp='null'
        ServiceConfigObject.save()

    ServiceDelDict = {"code": 20000, "data": {'Issuccess': 'Success'}}
    ServiceDelDictJson = json.dumps(ServiceDelDict, ensure_ascii=False)
    return HttpResponse(ServiceDelDictJson)


def ServiceVpc(request):
    vpcList=[]
    subnetList=[]
    vpclist = vpc.vpc()
    vpcxmlresult = vpclist.getALLXMLVpc()

    if type(vpcxmlresult) is list:
        for i in range(len(vpcxmlresult)):
            vpcxmldict = {'vpcid': vpcxmlresult[i]['vpcId'], 'cidrBlock': vpcxmlresult[i]['cidrBlock']}
            vpcList.append(vpcxmldict)
    else:
        vpcxmldict = {'vpcid': vpcxmlresult['vpcId'], 'cidrBlock': vpcxmlresult['cidrBlock']}
        vpcList.append(vpcxmldict)
    ServiceConfigObject = ServiceConfig.objects.all()[0]
    vpclist={"code":20000,"data":{"vpc":vpcList,'sip':ServiceConfigObject.ServiceSipIp}}


    VpcJson = json.dumps(vpclist, ensure_ascii=False)
    # print(VpcJson)
    return HttpResponse(VpcJson)

def ServiceSubnet(request):
    PostBody = request.body.decode('UTF-8')
    VPCID=str(PostBody)
    SubnetObject = vpc.vpc()
    SubnetObjectResult=SubnetObject.getXMLSubnet(VPCID)
    SubnetDictList=[]

    if type(SubnetObjectResult) ==list:
        for subnet in SubnetObjectResult:
            SubnetDict = {'vpcid': VPCID,
                          'subnetid': subnet['subnetId'], 'cidrBlock':subnet['cidrBlock']}
            SubnetDictList.append(SubnetDict)

    else:
        SubnetDict={'vpcid':VPCID,'subnetid':SubnetObjectResult['subnetId'],'cidrBlock':SubnetObjectResult['cidrBlock']}
        SubnetDictList.append(SubnetDict)


    subnetdict = {"code": 20000, "data": {'subnet': SubnetDictList}}
    SubnetJson = json.dumps(subnetdict, ensure_ascii=False)
    return HttpResponse(SubnetJson)

#{'ServiceIMC': 'SIP', 'ServiceName': '自助服务平台', 'ServiceDate': '2019-06-06 09:43:41', 'ServiceProcess': 0, 'ServiceIsInstall': False, 'ServiceStatus': '安装中', 'ServiceImage': F72A', 'ServiceTempImage': 'null', 'ServiceIp': None, 'vpcid': 'vpc-192093', 'SipIp': '', 'ServiceNum': '1'}

def JiSuanRoute(a,network):
   
    a_bin=bin(a)
    a_str=str(a_bin)
    a_str=a_str[2:len(a_str)]
    a_len=len(a_str)

    a_len_zheng=a_len//8
    a_len_yu=a_len%8

    a_len_zheng_new=0
    if a_len_yu != 0:
        a_len_zheng_new=a_len_zheng+1
    else:
        a_len_zheng_new=a_len_zheng

    a_str_list=[]

    for i in range(a_len_zheng_new):
        if i ==0 and a_len_zheng_new !=a_len_zheng:
            a_str_list.append(a_str[0:a_len_yu])
        else:
            
            a_str_list.append(a_str[a_len_yu:a_len_yu+8])
            a_len_yu+=8

    subnetlist=[]

    for strs in a_str_list:

        strs_len=len(strs)
        strs_list=list(strs)
        num=0
        for i in range(len(strs_list)):
            if strs_list[i] == '1':
                num+=pow(2,strs_len-int(i)-1)

        subnetlist.append(num)

    networklist=network.split('/')
    network_sublist=networklist[0].split('.')


    netmask=networklist[-1]
    str_netmask=[]
    for i in range(32):
        if int(i) >= int(netmask):
            str_netmask.append('0')
        else:
            str_netmask.append('1')

    netmask_list=[]
    for i in range(4):
        num=0
        for j in range(int(i)*8,(int(i)+1)*8):
        
            if str_netmask[j] == '1':
                num+=pow(2,7-int(j)%8)
        netmask_list.append(num)


    network_mask=''
    subnetlist_len=len(subnetlist)
    for i in range(4):
        network=network_sublist[i]
        netmask=netmask_list[i]
        xiangyu=int(network) & netmask
        if i >= 4-subnetlist_len:
            network_mask=network_mask+str(xiangyu+subnetlist[i*(subnetlist_len-1)//3])
        else:
            network_mask=network_mask+str(int(network) & netmask)
        if i!=3:
            network_mask=network_mask+'.'


    return network_mask



def ServiceInstall(request):
    ServicieDictBody = request.body.decode('UTF-8')
    # ServicieDictBodyString="'"+ServicieDictBody+"'"
    ServicieDictBodyString = ServicieDictBody

    ServicieDictString=ServicieDictBodyString.replace('false','"false"')

    ServiceDict=json.loads(ServicieDictString)
    SubnetObject = vpc.vpc()
    SubnetObjectResult = SubnetObject.getXMLSubnet(ServiceDict.get('vpcid'))
    route_network=''

    if ServiceDict.get("subnetid")  == None and type(SubnetObjectResult) == list:
        for subnet in SubnetObjectResult:
            ServiceDict.update({'subnetid': subnet['subnetId']})
            worknet=SubnetObjectResult['cidrBlock']
            network=SubnetObjectResult['network']
            route=SubnetObjectResult['router']
            network_host_num=int(route)-int(network)
            route_network=JiSuanRoute(network_host_num,worknet)
                
    else:
        ServiceDict.update({'subnetid': SubnetObjectResult['subnetId']})
        worknet=SubnetObjectResult['cidrBlock']
        network=SubnetObjectResult['network']
        route=SubnetObjectResult['router']
        network_host_num=int(route)-int(network)
        route_network=JiSuanRoute(network_host_num,worknet)
    ServiceDict.update({'route':route_network})



    AuthenticationJson=Authentication.objects.all()
    for authobject in  AuthenticationJson:
        ServiceDict.update({"ServiceAccessKey":authobject.ServiceAccessKey,"ServiceSecurityKey":authobject.ServiceSecurityKey})
    #
    ServiceConfigJson=ServiceConfig.objects.all()
    for ServiceObject in ServiceConfigJson:
        if ServiceObject.ServiceSipIp != ServiceDict.get('SipIp'):
            ServiceObject.ServiceSipIp=ServiceDict.get('SipIp')
            ServiceObject.save()
        ServiceConfigDict = model_to_dict(ServiceObject)
        ServiceDict.update(ServiceConfigDict)
    #
    # ServiceDict.update(AuthenticationDict)
    # ServiceDict.update(ServiceConfigDict)

    ServiceDict.update({'ServiceCloudIp':cloudutil.bcclient().getCfg().getEndpoint()})
    ServiceDict.update({'Option':"install"})

    CloudClientObject=CloudClient.CloudClient()
    ServiceDictJson=json.dumps(ServiceDict)
    HandleResult=CloudClientObject.HandleCloudService(ServiceDictJson,ServiceDict['ServiceIMC'],ServiceDict['ServiceImage'],'install')
    HandleResult=[HandleResult]
    CloudClientObject = {'code': 20000, 'data': {'items': HandleResult}}

    CloudClientObject = json.dumps(CloudClientObject, ensure_ascii=False)

    return HttpResponse(CloudClientObject)


def ServiceDiskStatus(request):
    #
    CloudDiskInfoObject=CloudDisk.CloudDisk()
    CloudDiskInfoObject.ceph_osd_position()
    CloudDiskInfoObject.GetHostIp()
    CloudDiskInfoObject.GetDiskInfo()
    CloudDiskInfoList=CloudDiskInfoObject.GetDiskInfoDictList()
    ServiceWrite=ServiceDisk.objects.get(ServiceDiskId=0)
    osdSum=0
    ErrorSum=0
    for CloudDiskInfo in CloudDiskInfoList:
        if CloudDiskInfo.get('osd') is not '':
            osdSum=osdSum+1
        if CloudDiskInfo.get('MediaError') > '0' or  CloudDiskInfo.get('OtherError') > '0':
            ErrorSum=ErrorSum+1
    ServiceWrite.ServiceDiskNum=len(CloudDiskInfoList)
    ServiceWrite.ServiceDiskErrorNum=ErrorSum
    ServiceWrite.ServiceDiskOsdNum=osdSum
    ServiceWrite.save()
    CloudDiskInfoDict={'code':20000,'data':{'items':CloudDiskInfoList}}
    CloudDiskInfoDictJson = json.dumps(CloudDiskInfoDict, ensure_ascii=False)
    return HttpResponse(CloudDiskInfoDictJson)


def GetDiskNum(request):
    DiskNumObject=CloudDiskNum.CloudDiskNum()
    DiskNumObjectDisk=DiskNumObject.CloudDiskSum()
    OSDSum=DiskNumObject.CloudOSDNum()-3
    ErrorSum=DiskNumObject.CloudErrorSum()
    ServiceList = Service.objects.all();
    ServiceNum=0
    for ServiceObject in ServiceList:
        if ServiceObject.ServiceStatus is True:
            ServiceNum=ServiceNum+1

    ServiceDiskObject = ServiceDisk.objects.all()[0]
    ServiceDiskObject.ServiceDiskNum=DiskNumObjectDisk
    ServiceDiskObject.ServiceDiskErrorNum=ErrorSum
    ServiceDiskObject.ServiceDiskOsdNum=OSDSum
    ServiceDiskObject.save()

    DiskNumDict={'code':20000,'data':{'ServiceDiskNum':DiskNumObjectDisk,"ServiceDiskErrorNum":ErrorSum,"ServiceDiskOsdNum":OSDSum,"ServiceNum":ServiceNum}}
    DiskNumDictJson = json.dumps(DiskNumDict, ensure_ascii=False)
    return HttpResponse(DiskNumDictJson)

def ServiceCancel(request):
    PostBody = request.body.decode('UTF-8')
    ServiceDict = json.loads(PostBody)
    ServiceDict.update({'Option': "cancel"})
    CloudClientObject = CloudClient.CloudClient()
    ServiceDictJson = json.dumps(ServiceDict)
    HandleResult = CloudClientObject.HandleCloudService(ServiceDictJson, ServiceDict['ServiceIMC'],
                                                        ServiceDict['ServiceImage'],'cancel')

    if HandleResult.get('ServiceResult') ==True:
        ServiceObject=Service.objects.get(ServiceIMC=ServiceDict.get('ServiceIMC'))
        ServiceObject.ServiceProcess=0
        ServiceObject.ServiceStatus=0
        ServiceObject.ServiceOption='0'
        ServiceObject.save()
    CloudClientObject = {'code': 20000, 'data': {'Issuccess': 'Success'}}

    CloudClientObject = json.dumps(CloudClientObject, ensure_ascii=False)
    return HttpResponse(CloudClientObject)



