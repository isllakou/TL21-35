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
            #Get Passes by id and date_from, date_to
            date1 = datetime.strptime(date_from, "%Y%m%d")
            date2 = datetime.strptime(date_to, "%Y%m%d")

            passes = Passes.objects.filter(stationRef = station_id, timestamp__gte = date1, timestamp__lte = date2)

            response = serializers.serialize("json", passes)

            #General Information
            get_info = {
                "Station" : station_id,
                "StationOperator" : Station.objects.get(stationID = station_id).stationProvider,
                "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
                "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
                "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
                "NumberOfPasses" : len(passes)
                }

            #Pass List
            pass_list = []
            i = 0
            pass_list.append(("PassIndex", "PassId", "PassTimeStamp" , "VevicleID" , "TagProvider", "PassType", "PassCharge"))
            for obj in passes:
                i = i + 1
                tag_provider = Vehicle.objects.get(vehicleID = obj.vehicleRef).providerAbbr

                #station_ref = obj.stationRef[:2]
                station_ref = obj.stationRef
                str2 = str(station_ref)
                str3= str2[16:18]

                if(tag_provider==str3):
                    pass_type = "home"
                else:
                    pass_type = "visitor"

                pass_list.append((i, obj.passID, obj.timestamp.strftime("%Y/%m/%d %H:%M:%S"), obj.vehicleRef, tag_provider, pass_type, obj.charge, str3))

            response = (get_info.items(), pass_list)
            return HttpResponse(response, content_type='application/json')

#Endpoint 2
def passes_analysis(request, op1_ID, op2_ID, date_from, date_to):
    date1 = datetime.strptime(date_from, "%Y%m%d")
    date2 = datetime.strptime(date_to, "%Y%m%d")
    passes = Passes.objects.filter(stationRef = op1_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = op2_ID)
    response = serializers.serialize("json", passes)

    List = []
    i = 0
    for obj in passes:
        i = i + 1

        List.append(({"PassIndex":i, "PassId":obj.passID, "StationID":obj.providerAbbr, "timestamp":obj.timestamp.strftime("%Y/%m/%d %H:%M:%S"), "VevicleID":obj.vehicleRef, "Charge":str(obj.charge)}))
    print(List)
    get_info = {
        "op1_ID" : op1_ID,
        "op2_ID" : op2_ID,#Station.objects.get(stationID = station_id).stationProvider,
        "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
        "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
        "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
        "NumberOfPasses" : len(passes),
         "PassesList" : List
        }

    response = json.dumps(get_info)
    return HttpResponse(response, content_type='application/json')
