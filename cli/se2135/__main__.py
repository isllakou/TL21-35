import click
import requests


@click.group()
def main():
    '''
    Main Commands to manage your database
    '''
    pass


@click.group(name='post')
def admin_group():
    '''
    Group for admin Endpoints
    '''
    pass

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


@click.group(name='get')
def basic_group():
    '''
    Group for basic endpoints
    '''
    pass

@click.command(name='passesperstation')
@click.option('--station_id', help="Συμπληρώστε το id του σταθμού!", type=str, required=True)
@click.option('--date_from', help="Συμπληρώστε την αρχική χρονική περίοδο", required=True)
@click.option('--date_to', help="Συμπληρώστε την τελική χρονική περίοδο", required=True)
@click.option('--format', help="Συμπληρώστε το format των δεδομένων(json|csv)", required=True, default='json')

def passes_per_station(station_id, date_from, date_to, format):#, _from, _to, _format):
    url = 'http://localhost:9103/interoperability/api/PassesPerStation/'+str(station_id)+'/'+str(date_from)+'/'+str(date_to)+'?format='+str(format)
    result = requests.get(url)
    if format == 'csv':
        url_content = result.content
        csv_file = open('downloaded.csv', 'wb')

        csv_file.write(url_content)
        csv_file.close()
    else:
        result_dict = result.json()
        click.echo(result_dict)
        # print(result_dict)


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
        url_content = result.content
        csv_file = open('downloaded.csv', 'wb')

        csv_file.write(url_content)
        csv_file.close()
    else:
        result_dict = result.json()
        click.echo(result_dict)


admin_group.add_command(reset_stations)
admin_group.add_command(reset_passes)
admin_group.add_command(reset_vehicles)
basic_group.add_command(passes_per_station)
basic_group.add_command(passes_analysis)

main.add_command(admin_group)
main.add_command(basic_group)
