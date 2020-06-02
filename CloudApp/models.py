from django.db import models

# Create your models here.

class Service(models.Model):
    ServiceIMC = models.CharField(max_length=10,primary_key=True)
    ServiceName= models.CharField(max_length=20,null=True)
    ServiceDate=models.DateTimeField()
    ServiceProcess=models.IntegerField()
    ServiceIsInstall=models.BooleanField()
    ServiceStatus=models.NullBooleanField()
    ServiceImage=models.CharField(max_length=12,null=True)
    ServiceTempImage=models.CharField(max_length=12)
    ServiceIp=models.CharField(max_length=25)
    ServiceOption=models.CharField(max_length=50)

    def __str__(self):
        return self.ServiceIMC
    

class ServiceLog(models.Model):
    ServiceIMC=models.ForeignKey("Service",on_delete=True)
    ServiceOptionDate=models.DateTimeField(auto_now=True)
    ServiceOptionName=models.CharField(max_length=20)
    ServiceOption=models.TextField()
    ServiceOptionIsSuccess=models.BooleanField()

class Authentication(models.Model):
    ServiceAccessKey=models.CharField(max_length=30)
    ServiceSecurityKey=models.CharField(max_length=60)
    ServiceToken=models.CharField(max_length=20)
    ServiceTokenTime=models.DateTimeField()

    def __str__(self):
        return self.ServiceAccessKey

class ServiceConfig(models.Model):
    ServiceId=models.IntegerField(primary_key=True,auto_created=True)
    ServiceSipIp=models.CharField(max_length=30)
    ServiceEcrIp=models.CharField(max_length=30)
    ServiceRootPassword=models.CharField(max_length=30)
    ServiceBingoPassword=models.CharField(max_length=30)
    ServiceModDate=models.DateTimeField(auto_now=True)
    ServiceIsUser=models.BooleanField()

class ServiceDisk(models.Model):
    ServiceDiskId = models.IntegerField(primary_key=True, auto_created=True)
    ServiceDiskNum=models.CharField(max_length=10)
    ServiceDiskErrorNum=models.CharField(max_length=10)
    ServiceDiskOsdNum=models.CharField(max_length=10)
    ServiceDiskDate=models.DateTimeField(auto_now=True)


