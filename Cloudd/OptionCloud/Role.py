import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
from util import xmltodict,cloudutil

class Role():
    def __init__(self,client):
        self.client=client
    def CreateRole(self,ServiceId):
        RoleID=self.GetRole(ServiceId)
        if RoleID is "1":
            params={"roleName":ServiceId,'GenerateInstanceProfile':True,'Path':'/'}
            Roleresult=self.client.invoke("CreateRole",params)
            XMLRoleresultInfo = xmltodict.parse(Roleresult, encoding='utf-8')
            return XMLRoleresultInfo['CreateRoleResponse']['CreateRoleResult']['Role']['RoleName']
        else:
            return RoleID

    def RoleModPower(self,ServiceId):
        # policy={"Statement":{"Effect":"Allow","Action":"*","Resource":"*"}}
        policy='{"Statement": [{"Effect": "Allow","Action": "*","Resource": "*"}]}'
        params={"PolicyDocument":policy,'PolicyName':ServiceId,'RoleName':ServiceId}
        result=self.client.invoke("PutRolePolicy",params)


    def GetRolePolicy(self):
        params={"RoleId":"role-769EFBDF4907A01677424F90F176D6547E69009A",'RoleName': 'dkoie','PolicyName': "dkoie"}
        result=self.client.invoke("GetRolePolicy",params)


    def GetRole(self,ServiceId):
        params={"RoleName":ServiceId}
        RoleResult=self.client.invoke("GetRole",params)

        try:
            XMLRoleresultInfo = xmltodict.parse(RoleResult, encoding='utf-8')
            result=XMLRoleresultInfo["GetRoleResponse"]["GetRoleResult"]["Role"]["RoleName"]
            return result
        except Exception as e:
            return "1"
    def GetRoleList(self):

        try:
            RoleList = self.client.invoke("ListRoles", {})
            XMLRoleresultInfo = xmltodict.parse(RoleList, encoding='utf-8')

            result = XMLRoleresultInfo["ListRolesResponse"]["ListRolesResult"]["Roles"]["member"]
            return result
        except Exception as e:

            return "1"

    def DelRole(self,RoleName):
        RoleId=self.GetRole(RoleName)
        if RoleId == '1':
            return False
        param={"RoleId":RoleId}
        DelResult=self.client.invoke("DeleteRole",param)
        return True

# if __name__== '__main__':
#     reole=Role()
#     reole.DelRole(reole.GetRole('sdn'))