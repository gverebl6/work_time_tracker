import csv 
import os
from datetime import datetime

from workHours.models import Hour


class HourService:

    def __init__(self, table):
        self.table = table
    
    # Adds an hour record
    def add_hour(self, work_hour):
        with open(self.table, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=Hour.schema())
            writer.writerow(work_hour.to_dict())

    #Returns the table's content
    def get_hours(self, prev=None, year=None, week=None):
        
        current_time = self.get_current_time()
        
        filters = {
            'week' : current_time['week'],
            'year' : current_time['year']
        }
        #print(type(filters['week']))
        if prev: 
            if filters['week'] == 0:
                filters['week'] = 52
                filters['year'] = filters['year'] - 1
            else:
                filters['week'] = filters['week'] - 1
        elif week:
            filters['week'] = week
            if year:
                filters['year'] = year
            

        with open(self.table, mode='r') as f:
            data_dict = csv.DictReader(f, fieldnames=Hour.schema())
            data = []
            
            for elem in data_dict:
                data.append(list(elem.values()))
        
        return data

        
        
        
                
            
    
    @staticmethod
    def get_current_time():
        return {
            'week': int(datetime.now().strftime("%V")),
            'day':  int(datetime.now().weekday()),
            'year': int(datetime.now().year)
        }