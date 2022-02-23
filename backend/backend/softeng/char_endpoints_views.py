from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from datetime import datetime
import json
import csv
import pandas as pd
from .models import *

#Function to calculate costs between two operators
def calculate_cost_betweentwo_operators(op1_ID, op2_ID, date_from, date_to):
    passes = Passes.objects.filter(stationRef__stationID__startswith = op1_ID, timestamp__gte = date_from, timestamp__lte = date_to, providerAbbr = op2_ID)
    cost1 = 0
    for obj in passes:
        cost1 += obj.charge

    passes = Passes.objects.filter(stationRef__stationID__startswith = op2_ID, timestamp__gte = date_from, timestamp__lte = date_to, providerAbbr = op1_ID)
    cost2 = 0
    for obj in passes:
        cost2 += obj.charge

    cost = cost1 - cost2
    if cost < 0:
        cost = 0

    return cost


#Endpoint a
def passes_per_station(request, station_id, date_from, date_to):
#Get Passes by id and date_from, date_to
    format = request.GET.get('format')
    date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
    date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)

    passes = Passes.objects.filter(stationRef = station_id, timestamp__gte = date1, timestamp__lte = date2)

    List = []
    i = 0
    for obj in passes:
        i = i + 1

        provider = obj.stationRef.stationProvider
        abbr = Operator.objects.get(tagProvider = provider).provider_ID

        if(obj.providerAbbr == abbr):
            pass_type = "home"
        else:
            pass_type = "visitor"

        List.append(({"PassIndex":i, "PassId":obj.passID, "PassTimeStamp":obj.timestamp.strftime("%Y/%m/%d %H:%M:%S") ,"VevicleID":obj.vehicleRef, "TagProvider":obj.providerAbbr, "PassType":pass_type, "PassCharge":str(obj.charge)}))

    if format == 'csv':
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="PassesPerStation.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['PassIndex', 'PassId', 'PassTimeStamp', 'VevicleID', 'TagProvider', 'PassType', 'PassCharge'])
        for i in List:
            writer.writerow([i['PassIndex'], i['PassId'], i['PassTimeStamp'], i['VevicleID'], i['TagProvider'], i['PassType'], i['PassCharge']])

        return response

    elif format == 'json' or 'None':
        get_info = {
            "Station" : station_id,
            "StationOperator" : Station.objects.get(stationID = station_id).stationProvider,
            "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
            "NumberOfPasses" : len(passes),
            "PassesList": List
            }

        response = json.dumps(get_info)
        return HttpResponse(response, content_type='application/json')


#Endpoint b
def passes_analysis(request, op1_ID, op2_ID, date_from, date_to):
    format = request.GET.get('format')
    date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
    date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
    passes = Passes.objects.filter(stationRef__stationID__startswith = op1_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = op2_ID)

    List = []
    i = 0
    for obj in passes:
        i = i + 1

        List.append(({"PassIndex":i, "PassId":obj.passID, "StationID":obj.stationRef.stationID, "Timestamp":obj.timestamp.strftime("%Y/%m/%d %H:%M:%S"), "VevicleID":obj.vehicleRef, "Charge":str(obj.charge)}))

    if format == 'csv':
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="PassesAnalysis.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['PassIndex', 'PassId', 'StationID', 'Timestamp', 'VevicleID', 'Charge'])
        for i in List:
            writer.writerow([i['PassIndex'], i['PassId'], i['StationID'], i['Timestamp'], i['VevicleID'], i['Charge']])

        return response

    elif format == 'json' or 'None':
        get_info = {
            "op1_ID" : op1_ID,
            "op2_ID" : op2_ID,
            "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
            "NumberOfPasses" : len(passes),
             "PassesList" : List
            }

        response = json.dumps(get_info)
        return HttpResponse(response, content_type='application/json')


#Endpoint c
def passes_cost(request, op1_ID, op2_ID, date_from, date_to):
    format = request.GET.get('format')
    date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
    date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
    passes = Passes.objects.filter(stationRef__stationID__startswith = op1_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = op2_ID)
    cost = calculate_cost_betweentwo_operators(op1_ID, op2_ID, date1, date2)

    if format == 'csv':
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="PassesCost.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['NumberOfPasses', 'PassesCost'])
        writer.writerow([len(passes), cost])

        return response

    elif format == 'json' or 'None':
        get_info = {
            "op1_ID" : op1_ID,
            "op2_ID" : op2_ID,#Station.objects.get(stationID = station_id).stationProvider,
            "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
            "NumberOfPasses" : len(passes),
            "PassesCost" : str(cost)
            }

        response = json.dumps(get_info)
        return HttpResponse(response, content_type='application/json')



#Endpoint 2d
def charges_by(request, op_ID, date_from, date_to):
    format = request.GET.get('format')
    date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
    date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
    providers = Operator.objects.values('provider_ID')

    List = []
    for i in providers:
        cost = 0
        j = 0

        if str(i['provider_ID']) == str(op_ID):
            continue

        passes = Passes.objects.filter(stationRef__stationID__startswith = op_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = i['provider_ID'])
        cost = calculate_cost_betweentwo_operators(op_ID, i['provider_ID'], date1, date2)

        List.append(({"VisitingOperator":i['provider_ID'], "NumberOfPasses": len(passes), "PassesCost": str(cost)}))

    if format == 'csv':
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="PassesAnalysis.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['VisitingOperator', 'NumberOfPasses', 'PassesCost'])
        for i in List:
            writer.writerow([i['VisitingOperator'], i['NumberOfPasses'], i['PassesCost']])

        return response

    elif format == 'json' or 'None':
        get_info = {
            "op_ID" : op_ID,
            "RequestTimestamp" : datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodFrom" :date1.strftime("%Y/%m/%d %H:%M:%S"),
            "PeriodTo" :date2.strftime("%Y/%m/%d %H:%M:%S"),
            "PPOList" : List
            }

        response = json.dumps(get_info)
        return HttpResponse(response, content_type='application/json')
