from django.urls import path
import CloudApp.views
#项目层次的路由设置

urlpatterns = [
    path('Auth', CloudApp.views.AuthenticationView),
    path('AuthInfo',CloudApp.views.AuthenticationViewInfo),
    path('ServiceList',CloudApp.views.ServiceList),
    path('ServiceUpdate',CloudApp.views.ServiceUpdate),
    path('ServiceInstall',CloudApp.views.ServiceInstall),
    path('ServiceVpc',CloudApp.views.ServiceVpc),
    path('ServiceSubnet',CloudApp.views.ServiceSubnet),
    path('ServiceUpdateProcess',CloudApp.views.ServiceUpdateProcess),
    path('ServiceDel',CloudApp.views.ServiceDel),
    path('ServiceCancel',CloudApp.views.ServiceCancel)
    #request获取参数
    #path('done1/<int:criteid>',djangoapp.vires.Dong1)
    #<datatype:参数>
]