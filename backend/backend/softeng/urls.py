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
    path('ChargesBy/<str:op_ID>/<str:date_from>/<str:date_to>', char_endpoints_views.charges_by)
    #4 characteristic endpoints
    #change this is wrong!
    # path('admin/PassesPerStation/:stationID/:date_from/:date_to/', views.PassesPerStation(stationID, date_from, date_to)),
    # path('admin/PassesPerStation', char_endpoints_views.PassesPerStation),

    # url(r'PassesPerStation', include(
    #     [url(r'(?P<stationID>\w+)', views.passesPerStation), url(r'(?P<date_from>\w+)', views.Date_From), url(r'(?P<date_to>\w+)', views.Date_To),
    # ])),

    #  url(r'admin/PassesPerStation/', include(
    #     [url(r'(?P<stationRef>\w+)', char_endpoints_views.PassesPerStation),
    # ]))

    #this works!




]
