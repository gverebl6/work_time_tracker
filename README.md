# Work Time Tracker

## Dependencies Docs

---

[Welcome to Click - Click Documentation (7.x)](https://click.palletsprojects.com/en/7.x/)

[Tabulate User Manual - Tabulate for WordPress 2.10.3 documentation](https://tabulate.readthedocs.io/en/latest/)

## Installation Guide

---

1. Download the project from GitHub

    [gverebl6/work_time_tracker](https://github.com/gverebl6/work_time_tracker)

2. Install the application:
    - In the app directory use:

        ```bash
        pip install --editable
        ```

    - Add alias to machine in the file .bash_aliases or .bashrc add the line

        ```bash
        alias tracker='/home/[username]/.local/bin/tracker'
        ```

## App use

---

This is used to track some work related data through a CLI interface.

### Hours service

This service is used to manage the hours worked by the user. With the following commands

<br><br>
#### Show command

`show`: Shows the table of registered hours 

default (no options or flags): Shows the current week's hours in short version

**flags**

`--prev`: Shows previous week

`--custom`: Prompts to ask for week and year to show 

`--complete`: Shows all data stored in the table.   

**options**

`--week, -w`: To choose the week to show. If -y is not used with this option, the selected week is from the current year.

`--year, -y`: To choose the year to show. Needs -w in order to work

<br><br>
#### Add command

`add`: Add a new record of hours worked in a day.

default (no options): Uses current year, month and day.

**arguments**

hours: Amount of hours worked to add.

minutes: Amount of minutes worked to add.

description: A description of work performed in that time.

**options**

`--year, -y`: Which year to add on.

`--week, -w`: Which week to add on

`--day, -d`: Which day to add on

<br><br>
#### Delete command

`delete`: Deletes a record from the database based on a record id

**argument**

hour_id: Id of the record in the database, either short or complete version 


<br><br>
#### Update command

`update`: Updates a record in order to change incorrect data on the record

**argument**

hour_id: Id of the record in the database, either short or complete version 

**options**

`--year, -y`: Which year to change to

`--week, -w`: Which week to change to.

`--day, -d`: Which day to change to.

`--hours, -h`: Amount of hours worked to update to

`--minutes, -m`: Amount of minutes to update to.

`--description, -l`: Description to update to. 

<br><br>
#### Count command

`count`: Generates a report with the worked hours reported for a specific range of weeks

**options:**

`--all`: Generates a report for all hours in the database 

`--week, -w`: Specific week to generate report to. 

`--start, -i`: A specific week to start counting (If no stop, stop=current week)

`--stop, -f`: The last week to count to (If no start, start = first week of year)

<br><br>
#### Current command

`current`: Displays current year, week and day number to help users to add new hours