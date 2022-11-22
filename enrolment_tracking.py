import csv
import pandas as pd
from datetime import datetime
from random import randint

enrolment = pd.DataFrame({'ID':[], 'Program':[], 'Location':[], 'Hours':[]})

## Importing Lessons Data
lessons = pd.read_csv('lessons.csv')

# Filtering Date Range of Enrolment Data
start_date = pd.to_datetime('2022-09-05 00:00:00')
end_date = pd.to_datetime('2023-01-01 00:00:00')

complete = lessons[(pd.to_datetime(lessons['DateTime']) > start_date) & (pd.to_datetime(lessons['DateTime']) < end_date) & (lessons['Status'] == 'Complete')]

take_home = lessons[(pd.to_datetime(lessons['DateTime']) > start_date) & (pd.to_datetime(lessons['DateTime']) < end_date) & (lessons['Status']== 'Complete: Take-Home')]

filtered = pd.concat([complete,take_home])


# Convert Homework Support & Explicit Instruction to 1-to-1 Instruction
filtered = filtered.replace('Explicit Instruction', '1-to-1 Instruction')
filtered = filtered.replace('Homework Support', '1-to-1 Instruction')

# Structuring Enrolment DataFrame
uniques = filtered['ID'].unique()
programs = filtered['Program'].unique()

for student in uniques:
    stu_data = filtered[(filtered['ID']==student)]
    line = pd.DataFrame({'ID':student},  index=[0])
    for program in programs:
        if stu_data[(stu_data['Program']==program)]["Hours"].sum() > 0:
            locations = stu_data[(stu_data['Program']==program)]['Location'].unique()
            for location in locations:
                hours = stu_data[(stu_data['Program']==program) & (stu_data['Location']==location)]["Hours"].sum()
                line = pd.DataFrame({'ID':student, 'Program':program, 'Location':location, 'Hours':hours},  index=[0])
                enrolment = pd.concat([enrolment,line])

# Outputting Results
enrolment.to_csv('test.csv', index=False)
print('Unique Students: ' + str(len(uniques)))
One2one_uniques = filtered[(filtered['Program'] == '1-to-1 Instruction')]['ID'].unique()
print('Unique 1-to-1 Students: ' + str(len(One2one_uniques)))

## Printing Unique Students for 2022
start_date = pd.to_datetime('2022-01-01 00:00:00')
end_date = pd.to_datetime('2023-01-01 00:00:00')
filtered_2022 = lessons[(pd.to_datetime(lessons['DateTime']) > start_date) & (pd.to_datetime(lessons['DateTime']) < end_date)]
uniques = filtered_2022['ID'].unique()
print('2022 Unique: ' + str(len(uniques)+19+8-1))
