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
        if row['status'] != 'Planned' and row['\ufeff"id"'] not in entries:
            # Program
            pro = ''
            for i in range(len(programs)):
                if pro_snip[i].lower() in row['topic'].lower():
                    pro = programs[i]
            if pro != '':
                # Location
                if pro != 'RISE at School':
                    for i in  range(len(locations)):
                        if locations[i] in row['location']:
                            loc = locations[i]
                else:
                    loc = row['location']

                hrs = float(row['units_raw'])
                if pro == 'LDS Access':
                    hrs = round(hrs,0)

                if pro == 'Summer RISE Intensive':
                    rate = ''
                else:
                    rate = float(row['charge_rate_1'])
            
                date = pd.to_datetime(row['start'], format='%d/%m/%Y %I:%M %p')

                if row['status'] == 'Complete' and 'take-home' in row['topic'].lower():
                    status = 'Complete: Take-Home'
                elif row['status'] == 'Complete' and 'no-show' in row['topic'].lower():
                    status = 'No-Show'
                else:
                    status = row['status']
        
                #Student Expections
                if row['recipient_id_1'] == '1785364' and pro == 'Explicit Instruction':
                    pro = 'RISE at School'
                    loc = 'KLEOS'
                if row['recipient_id_1'] == '1379956' and pro == 'Explicit Instruction':
                    pro = 'RISE at School'
                    loc = 'Lord Strathcona Elementary'
                if row['recipient_id_1'] == '1379956' and pro == 'Homework Support':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'
                if row['recipient_id_1'] == '1726975' and pro == 'Explicit Instruction':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'

                line = pd.DataFrame({'Entry':row['\ufeff"id"'],'ID':row['recipient_id_1'], 'Program':pro, 'Location':loc, 'Status': status,
                                 'Hours':hrs, 'Rate': rate, 'DateTime':date}, index=[0])
                lessons = pd.concat([lessons,line])
            else:
                print(row['topic'])
                
        # Updating Corrections to Lesson Statuses        
        elif row['\ufeff"id"'] in entries:
            if row['status'] == 'Complete' and 'take-home' in row['topic'].lower():
                status = 'Complete: Take-Home'
            elif row['status'] == 'Complete' and 'no-show' in row['topic'].lower():
                status = 'No-Show'
            else:
                status = row['status']
                    
            lessons.loc[(lessons['Entry'] == row['\ufeff"id"'], 'Status')] = status

    # Group Programs
        for j in range(len(group_pro)):
            if group_pro[j].lower() in row['topic'].lower() and row['status'] != 'Planned' and row['\ufeff"id"']+'_1' not in entries:
                for i in range(1,11):
                    try:
                        if row['recipient_'+str(i)] != '' and row['recipient_attendance_'+str(i)] == 'Attended':
                            for k in  range(len(locations)):
                                if locations[k] in row['location']:
                                    loc = locations[k]
                            date = pd.to_datetime(row['start'], format='%d/%m/%Y %I:%M %p')
                            
                            line = pd.DataFrame({'Entry':row['\ufeffid']+'_'+str(i),'ID':row['recipient_id_'+str(i)], 'Program':gro_convert[j],
                                                 'Location':loc, 'Status':row['status'], 'Hours':float(row['units_raw']), 'DateTime':date}, index=[0])
                            lessons = pd.concat([lessons,line])
                    except:
                        continue
            
## Updating CSV
lessons.to_csv('lessons.csv', index=False)
