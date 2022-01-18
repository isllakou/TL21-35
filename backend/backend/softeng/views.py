from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django import forms
from django.core import serializers
import sampledata01
import json
import pandas as pd
from .models import *
from datetime import datetime

#ex : timestamp = 1/1/2019 01:33
def get_timestamp(timestamp):
    date_time = timestamp.split(" ")

    date = date_time[0].split("/")
    time = date_time[1].split(":")

    timestamp_field = datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]), 0, 0)
    return timestamp_field

def resetvehicles(request):
    if request.method == 'POST':
        #Change path
        df=pd.read_csv('sampledata01/sampledata01_vehicles_100.csv',sep=',')
        #print(df)
        Vehicle.objects.all().delete()
        row_iter = df.iterrows()

        objs = [

            Vehicle(

                vehicleID = row['vehicleID'],
                tagID = row['tagID'],


                tagProvider= (Operator.objects.get_or_create( provider_ID = row['providerAbbr'], tagProvider = row['tagProvider'])[0])

                ,
                providerAbbr = row['providerAbbr'],
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
        df=pd.read_csv('sampledata01/sampledata01_stations.csv',sep=';')
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
        df=pd.read_csv('sampledata01/sampledata01_passes100_8000.csv',sep=',')
        Passes.objects.all().delete()
        row_iter = df.iterrows()
        objs = [

            Passes(
                 passID = row['passID'],
                 timestamp = get_timestamp(row['timestamp']),
                 stationRef = (Station.objects.get_or_create( stationID = row['stationRef'])[0]),
                 vehicleRef = row['vehicleRef'],
                 charge = row['charge'],
                 providerAbbr = row['providerAbbr']
            )

            for index, row in row_iter

        ]

        if(objs):
            if(Passes.objects.bulk_create(objs)):
                response = JsonResponse({"status":"OK"}, safe=False)
                return response

            else:
                response = JsonResponse({"status":"failed"}, safe=False)
                return response

        response = JsonResponse({"status":"failed"}, safe=False)
        return response

    else:
        response = JsonResponse({"status":"failed"}, safe=False)
        return response

def healthcheck(request):
    return HttpResponse("hi")
