from django.http import HttpResponse
from http import HTTPStatus

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

# sort by PassTimestamp 
def pass_timestamp(elem):
    return elem["PassTimeStamp"]

# sort by PassTimestamp 
def pass_timestamp2(elem):
    return elem["Timestamp"]

#is date in format YYYYMMDD
def isdate(date):
    if(len(date)==8):
        if(0<int(date[4:6])<13 and 0<int(date[6:8])<32):
            return True
    return False

#Endpoint a
def passes_per_station(request, station_id, date_from, date_to):
    if(type(station_id)==str and len(station_id)==4 and isdate(date_from) and isdate(date_to) and int(date_from)<int(date_to)):
        #Get Passes by id and date_from, date_to
        format = request.GET.get('format')
        date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
        date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)

        passes = Passes.objects.filter(stationRef = station_id, timestamp__gte = date1, timestamp__lte = date2)
        if not passes:
            return HttpResponse(status=HTTPStatus.PAYMENT_REQUIRED)
        else:
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
            
                List.sort(key=pass_timestamp)

                if format == 'csv':
                    response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="PassesPerStation.csv"'},
                    )

                    writer = csv.writer(response)
                    writer.writerow(['PassIndex', 'PassId', 'PassTimeStamp', 'VevicleID', 'TagProvider', 'PassType'])
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
                    
                    return HttpResponse(response, status=HTTPStatus.OK,content_type='application/json')
    elif(type(station_id)!=str or len(station_id)!=4 or (not isdate(date_from)) or (not isdate(date_to)) or int(date_from)>int(date_to)):
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)


#Endpoint b
def passes_analysis(request, op1_ID, op2_ID, date_from, date_to):
    if(type(op1_ID)==str and type(op2_ID)==str and len(op1_ID)==2 and len(op2_ID)==2 and isdate(date_from) and isdate(date_to) and int(date_from)<int(date_to)):
        format = request.GET.get('format')
        date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
        date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
        passes = Passes.objects.filter(stationRef__stationID__startswith = op1_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = op2_ID)
        if not passes:
            return HttpResponse(status=HTTPStatus.PAYMENT_REQUIRED)
        else:
            List = []
            i = 0
            for obj in passes:
                i = i + 1

                List.append(({"PassIndex":i, "PassId":obj.passID, "StationID":obj.stationRef.stationID, "Timestamp":obj.timestamp.strftime("%Y/%m/%d %H:%M:%S"), "VevicleID":obj.vehicleRef, "Charge":str(obj.charge)}))

            List.sort(key=pass_timestamp2)

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

    elif(type(op1_ID)!=str or type(op2_ID)!=str or len(op1_ID)!=2 or len(op2_ID)!=2 or (not isdate(date_from)) or (not isdate(date_to)) or int(date_from)>int(date_to)):
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)


#Endpoint c
def passes_cost(request, op1_ID, op2_ID, date_from, date_to):
    if(type(op1_ID)==str and type(op2_ID)==str and len(op1_ID)==2 and len(op2_ID)==2 and isdate(date_from) and isdate(date_to) and int(date_from)<int(date_to)):
        format = request.GET.get('format')
        date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
        date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
        passes = Passes.objects.filter(stationRef__stationID__startswith = op1_ID, timestamp__gte = date1, timestamp__lte = date2, providerAbbr = op2_ID)
        
        if not passes:
            return HttpResponse(status=HTTPStatus.PAYMENT_REQUIRED)
        else:
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
    elif(type(op1_ID)!=str or len(op1_ID)!=2 or type(op2_ID)!=str or len(op2_ID)!=2  or (not isdate(date_from)) or (not isdate(date_to)) or int(date_from)>int(date_to)):
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)





#Endpoint 2d
def charges_by(request, op_ID, date_from, date_to):
    if(type(op_ID)==str and len(op_ID)==2 and isdate(date_from) and isdate(date_to) and int(date_from)<int(date_to)):
        format = request.GET.get('format')
        date1 = datetime.strptime(date_from, "%Y%m%d").replace(tzinfo=timezone.utc)
        date2 = datetime.strptime(date_to, "%Y%m%d").replace(tzinfo=timezone.utc)
        providers = Operator.objects.values('provider_ID')
        if not providers:
            return HttpResponse(status=HTTPStatus.PAYMENT_REQUIRED)
        else:
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
        
    elif(type(op_ID)!=str or len(op_ID)!=2 or (not isdate(date_from)) or (not isdate(date_to)) or int(date_from)>int(date_to)):
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

