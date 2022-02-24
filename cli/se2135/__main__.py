import click
import requests


@click.group()
def main():
    '''
    Main Commands to manage your database
    '''
    pass

#
# @click.group(name='post')
# def admin_group():
#     '''
#     Group for admin Endpoints
#     '''
#     pass

@click.command(name='resetstations')
def reset_stations():
    result = requests.post('http://localhost:9103/interoperability/api/admin/resetstations/')
    result_dict = result.json()
    click.echo(result_dict)


@click.command(name='resetpasses')
def reset_passes():
    result = requests.post('http://localhost:9103/interoperability/api/admin/resetpasses/')
    result_dict = result.json()
    click.echo(result_dict)


@click.command(name='resetvehicles')
def reset_vehicles():
    result = requests.post('http://localhost:9103/interoperability/api/admin/resetvehicles/')
    result_dict = result.json()
    click.echo(result_dict)

#
# @click.group(name='get')
# def basic_group():
#     '''
#     Group for basic endpoints
#     '''
#     pass

@click.command(name='passesperstation')
@click.option('--station_id', help="Συμπληρώστε το id του σταθμού!", type=str, required=True)
@click.option('--date_from', help="Συμπληρώστε την αρχική χρονική περίοδο", required=True)
@click.option('--date_to', help="Συμπληρώστε την τελική χρονική περίοδο", required=True)
@click.option('--format', help="Συμπληρώστε το format των δεδομένων(json|csv)", required=True, default='json')

def passes_per_station(station_id, date_from, date_to, format):#, _from, _to, _format):
    url = 'http://localhost:9103/interoperability/api/PassesPerStation/'+str(station_id)+'/'+str(date_from)+'/'+str(date_to)+'?format='+str(format)
    result = requests.get(url)
    if format == 'csv':
        click.echo(result.text)
    else:
        result_dict = result.json()
        click.echo(result_dict)


@click.command(name='passesanalysis')
@click.option('--op1_id', help="Συμπληρώστε το id του πρώτου σταθμού!", type=str, required=True)
@click.option('--op2_id', help="Συμπληρώστε το id του δεύτερου σταθμού!", type=str, required=True)
@click.option('--date_from', help="Συμπληρώστε την αρχική χρονική περίοδο", required=True)
@click.option('--date_to', help="Συμπληρώστε την τελική χρονική περίοδο", required=True)
@click.option('--format', help="Συμπληρώστε το format των δεδομένων(json|csv)", required=True, default='json')

def passes_analysis(op1_id, op2_id, date_from, date_to, format):
    url = 'http://localhost:9103/interoperability/api/PassesAnalysis/'+str(op1_id)+'/'+str(op2_id)+'/'+str(date_from)+'/'+str(date_to)+'?format='+str(format)
    result = requests.get(url)
    if format == 'csv':
        click.echo(result.text)
    else:
        result_dict = result.json()
        click.echo(result_dict)


@click.command(name='passescost')
@click.option('--op1_id', help="Συμπληρώστε το id του πρώτου σταθμού!", type=str, required=True)
@click.option('--op2_id', help="Συμπληρώστε το id του δεύτερου σταθμού!", type=str, required=True)
@click.option('--date_from', help="Συμπληρώστε την αρχική χρονική περίοδο", required=True)
@click.option('--date_to', help="Συμπληρώστε την τελική χρονική περίοδο", required=True)
@click.option('--format', help="Συμπληρώστε το format των δεδομένων(json|csv)", required=True, default='json')


def passes_cost(op1_id, op2_id, date_from, date_to, format):
    url = 'http://localhost:9103/interoperability/api/PassesCost/'+str(op1_id)+'/'+str(op2_id)+'/'+str(date_from)+'/'+str(date_to)+'?format='+str(format)
    result = requests.get(url)
    if format == 'csv':
        click.echo(result.text)
    else:
        result_dict = result.json()
        click.echo(result_dict)


@click.command(name='chargesby')
@click.option('--op_id', help="Συμπληρώστε το id του σταθμού!", type=str, required=True)
@click.option('--date_from', help="Συμπληρώστε την αρχική χρονική περίοδο", required=True)
@click.option('--date_to', help="Συμπληρώστε την τελική χρονική περίοδο", required=True)
@click.option('--format', help="Συμπληρώστε το format των δεδομένων(json|csv)", required=True, default='json')


def charges_by(op_id, date_from, date_to, format):
    url = 'http://localhost:9103/interoperability/api/ChargesBy/'+str(op_id)+'/'+str(date_from)+'/'+str(date_to)+'?format='+str(format)
    result = requests.get(url)
    if format == 'csv':
        click.echo(result.text)
    else:
        result_dict = result.json()
        click.echo(result_dict)


@click.command(name='admin')
@click.option('--passesupd', help="Πρόσθεση νέων Passes από αρχείο CSV", type=str, required=True)
@click.argument('source', type=click.File('r'))
# @click.option('--source', help="Aρχείο CSV", type=str, required=True)
def admin():
    df=pd.read_csv(source, sep=';')
    row_iter = df.iterrows()

    objs = [

        Passes(

             passID = row['passID'],
             timestamp = get_timestamp(row['timestamp']),
             stationRef = Station.objects.get(stationID = row['stationRef']),
             vehicleRef = row['vehicleRef'],
             charge = row['charge'],
             providerAbbr = row['providerAbbr']

        )

        for index, row in row_iter

    ]
    if(objs):
        if(Passes.objects.update_or_create(objs)):
            response = JsonResponse({"status":"OK"}, safe=False)
            click.echo(response)

        else:
            response = JsonResponse({"status":"failed"}, safe=False)
            click.echo(response)


main.add_command(reset_stations)
main.add_command(reset_passes)
main.add_command(reset_vehicles)
main.add_command(passes_per_station)
main.add_command(passes_analysis)
main.add_command(passes_cost)
main.add_command(charges_by)
main.add_command(admin)

# main.add_command(admin_group)
# main.add_command(basic_group)
