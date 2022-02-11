from django.urls import path, include, re_path
# from django.conf.urls import url
from . import views
from . import char_endpoints_views

# #URLConf
urlpatterns = [

    #4 first endpoints
    path('admin/resetstations/', views.resetstations),
    #path('admin/healthcheck/', views.healthcheck),
    path('admin/resetvehicles/', views.resetvehicles),
    path('admin/resetpasses/', views.resetpasses),

    
    #this works!
    path('PassesPerStation/<str:station_id>/<str:date_from>/<str:date_to>', char_endpoints_views.PassesPerStation),
    path('PassesAnalysis/<str:op1_ID>/<str:op2_ID>/<str:date_from>/<str:date_to>', char_endpoints_views.passes_analysis),
    path('PassesCost/<str:op1_ID>/<str:op2_ID>/<str:date_from>/<str:date_to>', char_endpoints_views.passes_cost),
    path('ChargesBy/<str:op_ID>/<str:date_from>/<str:date_to>', char_endpoints_views.charges_by),

    #exta endpoints
    path('getstations', char_endpoints_views.getstations)





]
