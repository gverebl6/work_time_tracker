import click
from tabulate import tabulate

from workHours.models import Hour
from workHours.services import HourService

@click.group()
def hour():
    """Manages the hour commands"""
    pass

# Show
@hour.command()
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
def show(ctx, prev, custom, year, week, complete):
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
    params = {'prev': False, 'week': None, 'year':None}
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

    #Normal and short prints
    if complete:
        print(tabulate(hour_table, headers=Hour.schema()))
    else: 
        hour_table = map( 
                lambda x: [x[0][:8]] + x[1:-1], # Shotens id and eliminates date_created
                hour_table)
        hour_table = list(hour_table)
        print(tabulate(hour_table, headers=Hour.schema()[:-1]))



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
        Adds a new hour for a day
            default: Adds on current day
            with options: 
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
@click.pass_context
def delete(ctx):
    """
        Delete an our based on argument id
    """
    #Usar un cheker de id con regex
    pass

#update
@hour.command()
@click.pass_context
def update(ctx):
    """
        Updates a specific record based on id
    """
    pass

# count
@hour.command()
@click.pass_context
def count(ctx):
    """
        Prints the sum of all hours in a week and generates
        a report based on the description of all days
            default: current
            options: 
                --week=n : For the nth week
                --multiweek=[n,m] : For the period of week n to m
                --all : For all the records
    """
    pass

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
