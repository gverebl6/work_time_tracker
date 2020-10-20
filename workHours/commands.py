from os import sep
import click
from click.termui import prompt
from tabulate import tabulate
#import uuid

from workHours.models import Hour
from workHours.services import HourService

@click.group()
def hour():
    """Manages the hour commands"""
    pass

# Show
@hour.command()
@click.option('--all', is_flag=True)
@click.option('--prev', is_flag=True)
@click.option('--custom', is_flag=True)
@click.option(
    '-y', '--year',
    type=int,
    help='Year to insert hours in'
)
@click.option(
    '-w', '--week',
    type=int,
    help='Week to insert hours in'
)
@click.option('--complete', is_flag=True)
@click.pass_context
def show(ctx, all, prev, custom, year, week, complete):
    """
        Shows all hours
            default: Current week's hours
            with options: 
                --prev: Prints previous week,
                --custom: Prompts to ask week and year
                --year=j: jth year
                --week=n : nth weeks hours
            if --year and/or --week are used, --custom is skipped
    """
    # Manage options
    params = {'all': False, 'prev': False, 'week': None, 'year':None}
    if all:
        params['all'] = True
    else:
        if prev:
            params['prev'] = True
        elif year or week:
            if year and not week:
                click.echo('Error: Year parameter recieved, week paramater also needed...')
                click.echo('\tTo send week parameter with year use <tracker hours show -y [n] -w [m]>')
                ctx.abort()
            else:
                params['week'] = week
                params['year'] = year
        elif custom:
            params['week'] = click.prompt('Which week? ', type=int, default=None)
            params['year'] = click.prompt('Which year? ', type=int, default=None)
    
    
    hour_service = HourService(ctx.obj['work_hours_table'])
    hour_table = hour_service.get_hours(**params)

    if hour_table:
        #Normal and short prints
        if complete:
            print(tabulate(hour_table, headers=Hour.schema()))
        else: 
            hour_table = map( 
                    lambda x: [x[0][:8]] + x[1:-1], # Shotens id and eliminates date_created
                    hour_table)
            hour_table = list(hour_table)
            print(tabulate(hour_table, headers=Hour.schema()[:-1]))
    else:
        print('-'*50 + '\nThere\'s no record for the date range requested')
        
    


#Add hour
@hour.command()
@click.option(
    '-y', '--year',
    type=int,
    help='Year to insert hours in'
)
@click.option(
    '-w', '--week',
    type=int,
    help='Week to insert hours in'
)
@click.option(
    '-d', '--day',
    type=int,
    help='Day of the week to insert hours in'
)
@click.argument('hours', type=int)
@click.argument('minutes', type=int)
@click.argument('description', type=str)
@click.pass_context
def add(ctx, year, week, day, hours, minutes, description):
    """
        Adds a new hour for a day\n
            default: Adds on current day\n
            with options:\n 
                --week=n, --day=m, --year=j: to insert as
    """
    
    work_hour = Hour(
        hours=hours,
        minutes=minutes,
        description=description,
        week=week,
        day=day,
        year=year
    )
    hour_service = HourService(ctx.obj['work_hours_table'])

    hour_service.add_hour(work_hour)
    
#delete
@hour.command()
@click.argument('record_id', type=str)
@click.pass_context
def delete(ctx, record_id):
    """
        Delete an our based on argument id
    """
    hour_service = HourService(ctx.obj['work_hours_table'])
    deleted = hour_service.delete_hour(record_id)
    if not deleted:
        click.echo(click.style('ERROR', bg='red'))
        click.echo('Operation error:')
        click.echo('No record found with the id you input.')
    elif len(deleted) == 1:
        click.echo(click.style('SUCCESS', bg='green'))
        click.echo(f'The record with id {deleted[0]} was successfully deleted.')
    else:
        click.echo(click.style('ERROR', bg='red'))
        click.echo('Operation error:')
        click.echo('There are more than one record that match your input.')
        click.echo(f'Try using the command <tracker hours uuid {record_id}> to get the specific id you want')
        
        


    

#update
@hour.command()
@click.argument('record_id', type=str)
@click.option(
    '-y', '--year',
    type=int,
    help='Year to update hours in'
)
@click.option(
    '-w', '--week',
    type=int,
    help='Week to update hours in'
)
@click.option(
    '-d', '--day',
    type=int,
    help='Day to update hours in'
)
@click.option(
    '-h', '--hours',
    type=int,
    help='Hour to update hours in'
)
@click.option(
    '-m', '--minutes',
    type=int,
    help='Minutes to update hours in'
)
@click.option(
    '-l', '--description',
    type=str,
    help='Minutes to update hours in'
)
@click.pass_context
def update(ctx, record_id, year=None, month=None, day=None, week=None, hours=None, minutes=None, description=None  ):
    """
        Updates a specific record based on id
    """
    hour_service = HourService(ctx.obj['work_hours_table'])

    update_options = {
        'year': year,
        'month': month,
        'week': week,
        'day': day,
        'hours': hours,
        'minute': minutes,
        'description': description
    }

    updated = hour_service.update_hour(record_id, update_options)
    if not updated:
        click.echo(click.style('ERROR', bg='red'))
        click.echo('Operation error:')
        click.echo('No record found with the id you input.')
    elif len(updated) == 1:
        click.echo(click.style('SUCCESS', bg='green'))
        click.echo(f'The record with id {updated[0]} was successfully updated.')
    else:
        click.echo(click.style('ERROR', bg='red'))
        click.echo('Operation error:')
        click.echo('There are more than one record that match your input.')
        click.echo(f'Try using the command <tracker hours uuid {record_id}> to get the specific id you want')


# count
@hour.command()
@click.option('--all', is_flag=True)
@click.option(
    '-w', '--week',
    type = int,
    help='Week to count the hours.'
)
@click.option(
    '-i', '--start',
    type = int,
    help='From which week to start counting'
)
@click.option(
    '-f', '--stop',
    type = int,
    help='Until which week to count'
)

@click.pass_context
def count(ctx, all, week, start, stop):
    """
        Prints the sum of all hours in a week and generates
        a report based on the description of all days
            default: current
            options: 
                --week=n : For the nth week
                --all : For all the records
                --start : from what week to start. 
                    (If no --to , then from that week to end)
                --stop : to what week to count 
                    (If no --from, then from begining to --to)
    """
    
    params = {'all': False, 'start': None, 'stop': None}
    if all:
        params['all'] = True
    else:
        if week:
            params['start'] = week
            params['stop'] = week
        else:
            if start:
                params['start'] = start
            if stop: 
                params['stop'] = stop
    
    hour_service = HourService(ctx.obj['work_hours_table'])
    
    table, work_time, report = hour_service.count_hours(**params)
    
    print('Period of work')
    hour_table = map( 
        lambda x: [x[0][:8]] + x[1:-1], # Shotens id and eliminates date_created
            table)
    hour_table = list(hour_table)
    print(tabulate(hour_table, headers=Hour.schema()[:-1]))

    print('\nTotal time worked: ')
    print(f'\t\t\t\tHours: {work_time[0]}\tMinutes: {work_time[1]}')

    print('\nActivities performed')
    print(*report, sep=', ')


# get uuid
@hour.command()
@click.argument('uuid_segment', type=str)
@click.pass_context
def uuid(ctx, uuid_segment):
    """ Returns the complete uuid from the first 4 digits """
    hour_service = HourService(ctx.obj['work_hours_table'])
    
    ids = hour_service.get_uuid(uuid_segment)

    if ids:

        if len(ids) > 1:
            click.echo('There are multiple possible ids, choose one to pipe with update or delete: ')
            for i, idx in enumerate(ids):
                click.echo(f'{i}. {idx}')
            option=click.prompt('Option', type=int)
            shortest_id = _get_short_uuid(option, ids)
            click.echo(f'The shortest id possible is {shortest_id}')

        else:
            click.echo(ids[0])
    else:
        click.echo('No id found to match that pattern....')

def _get_short_uuid(option, uuids):
    """Returns the shortes possible uuid when more than one is possible"""
    top_len = 0
    for elems in zip(*uuids):
        if len(set(elems)) > 1:
            return uuids[option][:top_len+1]
        else:
            top_len += 1
    return uuids[option]




# Current time
@hour.command()
@click.pass_context
def current(ctx):
    """
        Prints the current year day and week
    """
    current_time = HourService.get_current_time()
    print('_'*50)
    print(f"\tCurrent year: {current_time['year']}\n\
        Current week: {current_time['week']}\n\
        Current day: {current_time['day']}")


#Maybe un get id porque el id ta muy largo a partir de un short

all = hour
