from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.core import serializers
import json
import pandas as pd
from .models import *
from datetime import datetime


#Endpoint 1
def PassesPerStation(request, station_id, date_from, date_to):

        try:
            date1 = datetime.strptime(date_from, "%Y%m%d")
            date2 = datetime.strptime(date_to, "%Y%m%d")
        
            passes = Passes.objects.filter(stationRef = station_id, timestamp__gte =date1, timestamp__lte =date2)
            
            response = serializers.serialize("json", passes)
            return HttpResponse(response, content_type='application/json')
            
        except BaseException:
            return JsonResponse({"status":"parameters not valid"}, safe=False )
