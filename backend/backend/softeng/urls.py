from django.urls import path
from . import views

# #URLConf
urlpatterns = [
    path('admin/resetstations/', views.resetstations),
    #path('admin/healthcheck/', views.healthcheck),
    path('admin/resetvehicles/', views.resetvehicles),
    path('admin/resetpasses/', views.resetpasses),


]
