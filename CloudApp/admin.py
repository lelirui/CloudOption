from django.contrib import admin
from CloudApp.models import  Service,ServiceConfig,ServiceLog,Authentication,ServiceDisk

# Register your models here.

admin.site.register(Service)
admin.site.register(ServiceConfig)
admin.site.register(ServiceLog)
admin.site.register(Authentication)
admin.site.register(ServiceDisk)