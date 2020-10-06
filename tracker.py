import click
from workHours import commands as work_commands

WORK_HOURS_TABLE = './data/hours.csv'

#Punto de entrada
@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj ={}
    ctx.obj['work_hours_table'] = WORK_HOURS_TABLE

cli.add_command(work_commands.all)