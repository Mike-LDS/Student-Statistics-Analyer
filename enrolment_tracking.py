import csv
import pandas as pd
from datetime import datetime
from random import randint

enrolment = pd.DataFrame({'ID':[], 'First Name':[], 'Last Name':[], 'Program':[], 'Location':[], 'Hours':[]})

## Importing Lessons Data
lessons = pd.read_csv('lessons.csv')

# Filtering Date Range of Enrolment Data
start_date = pd.to_datetime('2022-07-01 00:00:00')
end_date = pd.to_datetime('2022-09-01 00:00:00')

filtered = lessons[(pd.to_datetime(lessons['DateTime']) > start_date) & (pd.to_datetime(lessons['DateTime']) < end_date)]

uniques = filtered['ID'].unique()
programs = lessons['Program'].unique()

# Structuring Enrolment DataFrame
for student in uniques:
    stu_data = filtered[(filtered['ID']==student)]
    first_name = stu_data['First Name'].mode()[0]
    last_name = stu_data['Last Name'].mode()[0]
    line = pd.DataFrame({'ID':student, 'First Name':first_name, 'Last Name':last_name},  index=[0])
    for program in programs:
        if stu_data[(stu_data['Program']==program)]["Hours"].sum() > 0:
            locations = stu_data[(stu_data['Program']==program)]['Location'].unique()
            for location in locations:
                hours = stu_data[(stu_data['Program']==program) & (stu_data['Location']==location)]["Hours"].sum()
                line = pd.DataFrame({'ID':student, 'First Name':first_name, 'Last Name':last_name, 'Program':program, 'Location':location, 'Hours':hours},  index=[0])
                enrolment = pd.concat([enrolment,line])

# Outputting Results
enrolment.to_csv('test.csv', index=False)

## Printing Unique Students for 2022
start_date = pd.to_datetime('2022-01-01 00:00:00')
end_date = pd.to_datetime('2023-01-01 00:00:00')
filtered = lessons[(pd.to_datetime(lessons['DateTime']) > start_date) & (pd.to_datetime(lessons['DateTime']) < end_date)]
uniques = filtered['ID'].unique()
print(len(uniques)+19+8-1)
