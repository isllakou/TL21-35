from django.urls import path
from . import views

# #URLConf
urlpatterns = [
    path('admin/resetstations/', views.resetstations),
    #path('admin/healthcheck/', views.healthcheck),


]
