'''
Code to add additional lessons to the CSV file, lessons.csv, which contains lessons LDS starting in 13 Sept 2021
'''

import csv
import pandas as pd
from datetime import datetime
from random import randint

locations = ['East Van', 'North Van', 'RISE @ Home', 'LDS Access']
pro_snip = ['Explicit', 'Support', 'School', 'SLP', 'RISE TEAM', 'RISE Now', 'Summer Tutoring', 'LDS Access', 'Summer RISE','KTEA-3 Assessment']
programs = ['Explicit Instruction', 'Homework Support', 'RISE at School', 'SLP', 'RISE TEAM', 'RISE Now', 'Summer Tutoring', 'LDS Access', 'Summer RISE Intensive','KTEA-3 Assessment']

# Tracked Group Programs
group_pro = ['LDS Social Language Group', 'Early RISErs']
gro_convert = ['Social Language Group', 'Early RISErs - Spring']

## Load DataFrame
lessons = pd.read_csv('lessons.csv')

entries = lessons['Entry'].unique()

## Compiling Lessons Data
with open('appointments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['status'] == 'Complete' and row['\ufeff"id"'] not in entries:
            # Program
            pro = ''
            for i in range(len(programs)):
                if pro_snip[i].lower() in row['topic'].lower():
                    pro = programs[i]
            if pro != '':
                # Student Name
                name = row['recipient_1'].split(' ',1)
                # Location
                if pro != 'RISE at School':
                    for i in  range(len(locations)):
                        if locations[i] in row['location']:
                            loc = locations[i]
                else:
                    loc = row['location']
            
                date = pd.to_datetime(row['start'], format='%d/%m/%Y %I:%M %p')
        
                line = pd.DataFrame({'Entry':row['\ufeff"id"'],'ID':row['recipient_id_1'], 'First Name': name[0], 'Last Name': name[1], 'Program':pro, 'Location':loc,
                                 'Hours':float(row['units_raw']), 'DateTime':date}, index=[0])
                lessons = pd.concat([lessons,line])
            else:
                print(row['topic'])

    # Group Programs
        for j in range(len(group_pro)):
            if group_pro[j].lower() in row['topic'].lower() and row['status'] != 'Cancelled' and row['\ufeffid']+'_1' not in entries:
                for i in range(1,11):
                    try:
                        if row['recipient_'+str(i)] != '' and row['recipient_attendance_'+str(i)] == 'Attended':
                            name = row['recipient_'+str(i)].split(' ',1)
                            for k in  range(len(locations)):
                                if locations[k] in row['location']:
                                    loc = locations[k]
                            date = pd.to_datetime(row['start'], format='%d/%m/%Y %I:%M %p')
                            
                            line = pd.DataFrame({'Entry':row['\ufeffid']+'_'+str(i),'ID':row['recipient_id_'+str(i)], 'First Name': name[0], 'Last Name': name[1], 'Program':gro_convert[j],
                                                 'Location':loc,'Hours':float(row['units_raw']), 'DateTime':date}, index=[0])
                            lessons = pd.concat([lessons,line])
                    except:
                        continue

## Updating CSV
lessons.to_csv('lessons.csv', index=False)
