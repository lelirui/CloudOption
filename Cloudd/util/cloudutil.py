#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib,datetime,urlparse2,http.client,urllib.parse
import hmac,hashlib,base64
import subprocess
import pymysql

def mycmp(x, y):
    x0 = x.split("=")[0]
    y0 = y.split("=")[0]
    if x0 < y0:
        return -1
    if x0 == y0:
        return 0
    return 1

def doSignV2(cfg, data):

  #  res = urlparse2.urlparse(cfg.endpoint)
    res = urllib.parse.urlparse(cfg.endpoint)
    stringToSign = cfg.method + "\n"
    stringToSign += res.netloc + "\n"
    if res.path == "":
        stringToSign += "/\n"
    else:
        stringToSign += res.path + "\n"

    items = data.split("&")
    # items.sort(cmp=lambda x,y:mycmp(x,y))
 #   items=sorted(items,key=lambda x,y:mycmp(x,y))
    items=sorted(items)

    stringToSign += "&".join(items)
    # return base64.b64encode(hmac.new(cfg.secretKey, stringToSign, hashlib.sha256).digest())
    return base64.b64encode(hmac.new(bytes(cfg.secretKey,'utf-8'), bytes(stringToSign,'utf-8'), hashlib.sha256).digest())

def timeStamp():
    dt = datetime.datetime.utcnow().isoformat()
    return dt.split('.')[0] + ".000Z"

def time2str(dt):
    str = dt.isoformat()
    return str.split('.')[0] + ".000Z"

def gethost(url):
 #   res = urlparse2.urlparse(url)
    res = urllib.parse.urlparse(url)
    return res.netloc


class config():
    endpoint = "http://10.203.66.2"
    accessKey = "1"
    secretKey = "1"
    version = "2019-06-01"
    signVersion = "2"
    method = "POST"
    signMethod = "HmacSHA256"


    def getEndpoint(self):
        return self.endpoint

    def getAccessKey(self):
        return self.accessKey

    def getSecretKey(self):
        return self.secretKey

class GetMysqlPassword():
    def GetMysqlPassword(self):
        MysqlPasswordSub = subprocess.Popen(['cat /opt/bingocloud/latest/output/config/db.cfg  | grep ec2'], shell=True,stdout=subprocess.PIPE)
        MysqlPasswordSub.wait()
        MysqlPasswordSub = MysqlPasswordSub.stdout.read()
        MysqlPassword = str(MysqlPasswordSub, encoding="utf-8")
        MysqlPasswordList = MysqlPassword.split('\n')
        return MysqlPasswordList[0].split(',')[4].split('"')[1]

class Initconfig():
    def __init__(self):
        self.db = pymysql.connect("localhost", "bingocloud", GetMysqlPassword().GetMysqlPassword(), "CloudOption")

    def GetDate(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * from CloudApp_authentication")
        self.data = cursor.fetchone()
        self.db.close()

    def getAccessKey(self):
        return self.data[1]

    def getSecretKey(self):
        return self.data[2]





class bcclient():
    def __init__(self, confSection='cloud', debug=False):
        self.cfg = config()
        self.debug = debug
        Data=Initconfig()
        Data.GetDate()
        self.cfg.accessKey=Data.getAccessKey()
        self.cfg.secretKey=Data.getSecretKey()
        self.cfg.endpoint='http://'+self.GetHostIp()

        # self.cfg.endpoint = 'http://10.202.36.1'

    def GetHostIp(self):
        CloudDBCfgSub = subprocess.Popen([" ss -atnl | grep 6789 | awk '{print $4}' | cut -d ':' -f1"],shell=True,stdout=subprocess.PIPE)
        CloudDBCfgSub.wait()
        CloudDBCat = CloudDBCfgSub.stdout.read()
        CloudDBCat = str(CloudDBCat, encoding="utf-8")
        CloudCatFileList = CloudDBCat.split('\n')
        return CloudCatFileList[0]


    def invoke(self, action, params):
        data = urllib.parse.urlencode({"Action":action})
        if len(params) > 0:
            data += "&" + urllib.parse.urlencode(params)

        ts = timeStamp()
        commons = {"Timestamp":ts,"AWSAccessKeyId":self.cfg.accessKey,"Version":self.cfg.version,"SignatureVersion":self.cfg.signVersion,"SignatureMethod":self.cfg.signMethod}
        data += "&" + urllib.parse.urlencode(commons)

        signVal = doSignV2(self.cfg, data)
        data += "&" + urllib.parse.urlencode({"Signature":signVal})

        host = gethost(self.cfg.endpoint)

        if self.debug == True:
            print('%s?\n%s\n' % (self.cfg.endpoint, data))

        conn = http.client.HTTPConnection(host)
        conn.request(self.cfg.method, self.cfg.endpoint, data)

        response = conn.getresponse()
        return response.read()

    def getCfg(self):
        return self.cfg
