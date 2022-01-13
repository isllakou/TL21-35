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

def resetvehicles(request):
    if request.method == 'POST':
        #Change path
        df=pd.read_csv('/home/ioanna/Documents/TL21-35/backend/backend/sampledata01/sampledata01/sampledata01_vehicles_100.csv',sep=';')
        #print(df)
        Vehicle.objects.all().delete()
        row_iter = df.iterrows()


        # #create operators
        # ops = [
        #     Operator(
        #         provider_ID = row['providerAbbr'],

        #         tagProvider = row['tagProvider']
        #     )

        #     for index, row in row_iter
        # ]

        # tagPro = Operator.objects.get_or_create(ops)

        # print("Tag pro is:", tagPro)

        objs = [

            Vehicle(

                vehicleID = row['vehicleID'],
                tagID = row['tagID'],
            
                #tagProvider = Operator.objects.get_or_create( [ Operator( provider_ID = row['providerAbbr'], tagProvider = row['tagProvider']) ]) 
                tagProvider= (Operator.objects.get_or_create( provider_ID = row['providerAbbr'], tagProvider = row['tagProvider'])[0])
                #tagProvider = tagPro
                ,
                
                licenseYear = row['licenseYear']

            )

            for index, row in row_iter

        ]

        if(objs):
            if(Vehicle.objects.bulk_create(objs)):
                response = JsonResponse({"status":"OK"}, safe=False)
            else:
             response = JsonResponse({"status":"failed"}, safe=False)

        return response
    else:
        response = JsonResponse({"status":"failed"}, safe=False)
        return response

def resetstations(request):
    if request.method == 'POST':
        #Change path
        df=pd.read_csv('/home/ioanna/Documents/TL21-35/backend/backend/sampledata01/sampledata01/sampledata01_stations.csv',sep=';')
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

def resetpasses(request):
    if request.method == 'POST':
        #Change path
        df=pd.read_csv('/home/ioanna/Documents/TL21-35/backend/backend/sampledata01/sampledata01/sampledata01_passes100_8000.csv',sep=';')
        #print(df)
        Passes.objects.all().delete()
        row_iter = df.iterrows()

        objs = [

            Passes(

                 passID = row['passID'],
                 timestamp = row['timestamp'],
                 stationRef = row['stationRef'],
                 vehicleRef = row['vehicleRef'],
                 charge = row['charge']


            )

            for index, row in row_iter

        ]

        if(objs):
            if(Passes.objects.bulk_create(objs)):
                response = JsonResponse({"status":"OK"}, safe=False)
            else:
             response = JsonResponse({"status":"failed"}, safe=False)

        return response
    else:
        response = JsonResponse({"status":"failed"}, safe=False)
        return response


def healthcheck(request):
    return HttpResponse("hi")
