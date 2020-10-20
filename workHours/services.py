import csv 
import os
from datetime import datetime

from workHours.models import Hour


class HourService:

    def __init__(self, table):
        self.table = table

    def __read_hours(self):
        """Returns the records dictionaries"""
        with open(self.table, mode='r') as f:
            data_dict = csv.DictReader(f, fieldnames=Hour.schema())
            return [elem for elem in data_dict]
    


    # Adds an hour record
    def add_hour(self, work_hour):
        with open(self.table, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=Hour.schema())
            writer.writerow(work_hour.to_dict())



    #Returns the table's content
    def get_hours(self, all=None, prev=None, year=None, week=None):
        
        current_time = self.get_current_time()
        
        #Condition evaluation
        filters = {
            'week' : current_time['week'],
            'year' : current_time['year']
        }
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


        # Data retrieved
        data_dict = self.__read_hours()
        data = [] 
        for elem in data_dict:
            data.append(list(elem.values()))
        
        
        #Data filtering 
        if all:
            return data
        else: 
            return [
                row for row in data 
                if row[1] == str(filters['year'] )
                and row[2] == str(filters['week'])
            ]
            
    
    #Deletes a record
    def delete_hour(self, uid):
        """Deletes a record specified by user's input"""
        def delete(records, uid):
            kept = []
            for record in records:
                if record['id'] != uid:
                    kept.append(record)
            
            return kept
                    
        records = self.__read_hours()
        possible_delete = []
        for record in records:
            if uid in record['id']:
                possible_delete.append(record['id'])

        if not possible_delete: #empty
            return None
        elif len(possible_delete) > 1:
            return possible_delete
        else:
            kept_data = delete(records, possible_delete[0])
            self._save_to_disk(kept_data)
            return possible_delete

    #Update a recors
    def update_hour(self, record_id, options):
        def update(records, record_to_update, year, month, week, day, minute, hours, description):
            new_data = []
            for record in records:
                if record['id'] == record_to_update:
                    #Aqui hacer el update
                    new_record = record.copy()
                    if year:
                        new_record['year'] = year
                    if month:
                        new_record['month'] = month
                    if week:
                        new_record['week'] = week
                    if day:
                        new_record['day'] = day
                    if hours:
                        new_record['hours'] = hours
                    if minute:
                        new_record['minute'] = minute
                    if description:
                        new_record['description'] = description
                    new_data.append(new_record)
                else:
                    new_data.append(record)
            return new_data

        records = self.__read_hours()
        possible_update = []
        for record in records:
            if record_id in record['id']:
                possible_update.append(record['id'])
       
        if not possible_update: #empty
            return None
        elif len(possible_update) > 1:
            return possible_update
        else:
            new_data = update(records, possible_update[0], **options)
            self._save_to_disk(new_data)
            return possible_update            


    def _save_to_disk(self, hours):
        tmp_table_name = self.table + '.tmp'
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=Hour.schema())
            writer.writerows(hours)  
        os.remove(self.table)
        os.rename(tmp_table_name, self.table)        


    #Returns the uuid from at least 4 characcters
    def get_uuid(self, uuid_segment):
        """Returns complete uuid from segment"""
        records = self.__read_hours()

        possible_ids = []
        
        for record in records:
            if uuid_segment in record['id']:
                possible_ids.append(record['id'])
        
        return possible_ids

    
    # Counts all hours for a fixed amount of weeks
    def count_hours(self, all, start, stop):
        """ Returns a report for the weeks selected.
            This command can only be used within a year unless all is used."""
        
        current_time = self.get_current_time()
        # Interpreting the parameters
        if start and not stop:
            stop = current_time['week']
        if stop and not start:
            start = 0
        
        if not start and not stop:
            start = current_time['week']
            stop = current_time['week']

        # Getting the data
        data = self.__read_hours()

        # Filtering data from params 
        if all:
            filtered_data = data
        else:
            filtered_data = []
            for record in data:
                if int(record['week']) >= start and int(record['week']) <= stop:
                    filtered_data.append(record)
        

        #Transfrom data to print
        data_print = [] 
        for elem in filtered_data:
            data_print.append(list(elem.values()))

        # Count hours and get descriptions
        hours = 0 
        minutes = 0 
        descriptions = []
        for record in filtered_data:
            hours += int(record['hours'])
            minutes += int(record['minutes'])
            descriptions.append(record['description'])

        #Fix for extra minutes
        hours += minutes//60
        minutes = minutes%60 
    
        # Resulting time 
        worked_time = (hours, minutes)


        return data_print, worked_time, descriptions


            


        

    @staticmethod
    def get_current_time():
        return {
            'week': int(datetime.now().strftime("%V")),
            'day':  int(datetime.now().weekday()),
            'year': int(datetime.now().year)
        }