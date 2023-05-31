'''
Code to add additional lessons to the CSV file, lessons.csv, which contains lessons LDS starting in 13 Sept 2021
'''

import csv
import pandas as pd
from datetime import datetime
from random import randint

locations = ['East Van', 'North Van', 'RISE at Home', 'LDS Access']
pro_snip = ['Explicit', 'Support', 'School', 'SLP', 'RISE TEAM', 'RISE Now', 'Summer Tutoring', 'LDS Access', 'Summer RISE','KTEA-3 Assessment']
programs = ['Explicit Instruction', 'Homework Support', 'RISE at School', 'SLP', 'RISE TEAM', 'RISE Now', 'Summer Tutoring', 'LDS Access', 'Summer RISE Intensive','KTEA-3 Assessment']

# Tracked Group Programs
group_pro = ['LDS Social Language Group', 'Early RISErs']
gro_convert = ['Social Language Group', 'Early RISErs - Spring']

## Load DataFrame
lessons = pd.read_csv('lessons.csv')

entries = lessons['Entry'].unique()

## New Lessons
new_lessons = pd.DataFrame({'Entry':[], 'ID':[], 'Program':[], 'Location':[], 'Status': [], 'Hours':[], 'Rate': [], 'Instructor':[], 'DateTime':[]})

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
                    loc = 'LDS Access'
                if row['recipient_id_1'] == '1837644' and pro == 'Homework Support':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'
                if row['recipient_id_1'] == '1726975' and pro == 'Explicit Instruction':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'
                if row['recipient_id_1'] == '1604267' and pro == 'Homework Support':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'
                if row['recipient_id_1'] == '1621195' and pro == 'Explicit Instruction':
                    pro = 'RISE at School'
                    loc = 'SD 5/DL'
                if row['recipient_id_1'] == '1929127' and pro == 'Explicit Instruction':
                    loc = 'LDS Access'
                if row['recipient_id_1'] == '1822481' and pro == 'Explicit Instruction':
                    loc = 'LDS Access'
                if row['recipient_id_1'] == '1841389' and pro == 'Explicit Instruction':
                    loc = 'LDS Access'
                

                line = pd.DataFrame({'Entry':row['\ufeff"id"'],'ID':row['recipient_id_1'], 'Program':pro, 'Location':loc, 'Status': status, 'Hours':hrs, 'Rate': rate,
                                     'Instructor':row['contractor_id_1'], 'DateTime':date}, index=[0])
                new_lessons = pd.concat([new_lessons,line])
            else:
                print(row['topic'])
                
            new_lessons.loc[(new_lessons['ID'] == '2084303', 'ID')] = '1574698'
                
        # Updating Corrections to Lesson Statuses (Only for Take-Home)        
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
                            new_lessons = pd.concat([new_lessons,line])
                    except:
                        continue

## Checking for Subbed Lessons
for index, row in new_lessons.iterrows():
    if len(new_lessons[(new_lessons['DateTime'] == row['DateTime']) & (new_lessons['Instructor'] == row['Instructor'])]) > 1:
        if row['Status'] == 'Cancelled':
            new_lessons.loc[(new_lessons['Entry'] == row['Entry'], 'Status')] = 'Subbed'
            
## Updating CSV
lessons = pd.concat([lessons,new_lessons])
lessons.to_csv('lessons.csv', index=False)
