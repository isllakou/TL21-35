from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.core import serializers
#import csv
import json
import pandas as pd
from .models import *
new = [
 {
   "stationID": "AO00",
   "stationProvider": "aodos",
   "stationName": "aodos tolls station 00"
 },
 {
   "stationID": "AO01",
   "stationProvider": "aodos",
   "stationName": "aodos tolls station 01"
 }
 ]

# def resetstations(request):
#     if request.method == 'POST':
#         source = request.read()
#         # data = json.loads(source)
#         # ndata = json.dumps(data)
#         return HttpResponse(source.content)
#     else:
#         return HttpResponse("Nop")

def resetstations(request):
    if request.method == 'POST':
        df=pd.read_csv('sampledata01_stations.csv',sep=';')
        #print(df)
        Station.objects.all().delete()
        row_iter = df.iterrows()

        objs = [

            Station(

                stationID = row['stationID'],

                stationProvider  = row['stationProvider'],

                stationName  = row['stationName']

            )

            for index, row in row_iter

        ]

        if(objs):
            if(Station.objects.bulk_create(objs)):
                response = JsonResponse({"status":"OK"}, safe=False)
            else:
             response = JsonResponse({"status":"failed"}, safe=False)

        return response
    else:
        response = JsonResponse({"status":"failed"}, safe=False)
        return response


def healthcheck(request):
    return HttpResponse("hi")
