import uuid
from datetime import datetime

class Hour():

    def __init__(self, hours, minutes, description ,week=None, day=None, year=None , id=None, date_added=None):
        # Add required data 
        self.hours = hours
        self.minutes = minutes
        self.description = description
        self.id = id or uuid.uuid4()
        
        # Add creation data
        if not date_added:
            self.date_added = datetime.now()
        else:
            self.date_added = date_added

        #Specific optional data
        if not day:
            self.day = datetime.now().weekday()
        else:
            self.day=day

        if not week:
            self.week = datetime.now().strftime("%V")
        else:
            self.week = week

        if not year:
            self.year = datetime.now().year
        else:
            self.year = year

    def to_dict(self):
        return vars(self)
    
    @staticmethod
    def schema():
        return ['id', 'year', 'week', 'day', 'hours', 'minutes', 'description', 'date_added']