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

lessons = pd.DataFrame({'Entry':[], 'ID':[], 'First Name':[], 'Last Name':[], 'Program':[], 'Location':[], 'Status':[], 'Hours':[], 'Rate':[], 'DateTime':[]})

## Compiling Lessons Data
with open('appointments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['status'] != 'Planned':
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
        
                line = pd.DataFrame({'Entry':row['\ufeff"id"'],'ID':row['recipient_id_1'], 'First Name': name[0], 'Last Name': name[1], 'Program':pro, 'Location':loc, 'Status': row['status'],
                                 'Hours':float(row['units_raw']), 'Rate':float(row['charge_rate_1']), 'DateTime':date}, index=[0])
                lessons = pd.concat([lessons,line])
            else:
                print(row['topic'])

    # Group Programs
        for j in range(len(group_pro)):
            if group_pro[j].lower() in row['topic'].lower() and row['status'] != 'Planned':
                for i in range(1,11):
                    try:
                        if row['recipient_'+str(i)] != '' and row['recipient_attendance_'+str(i)] == 'Attended':
                            name = row['recipient_'+str(i)].split(' ',1)
                            for k in  range(len(locations)):
                                if locations[k] in row['location']:
                                    loc = locations[k]
                            date = pd.to_datetime(row['start'], format='%d/%m/%Y %I:%M %p')
                            
                            line = pd.DataFrame({'Entry':row['\ufeff"id"']+'_'+str(i),'ID':row['recipient_id_'+str(i)], 'First Name': name[0], 'Last Name': name[1], 'Program':gro_convert[j],
                                                 'Status': row['status'], 'Location':loc,'Hours':float(row['units_raw']), 'Rate':float(row['charge_rate_'+str(i)]), 'DateTime':date}, index=[0])
                            lessons = pd.concat([lessons,line])
                    except:
                        continue

# Adding Non-Lesson Based Group programs
group_programs = ['Spring Break Camps 2022', '2022 Early RISErs - Winter']
gro_convert = ['Spring Break Camps', 'Early RISEr - Winter']
hours_group = ['35','20']
start_dates = ['2022-03-14','2022-01-10']

with open('users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for i in range(len(group_programs)):
            if group_programs[i] in row['Labels']:
                date = pd.to_datetime(start_dates[i], format='%Y-%m-%d')
                line = pd.DataFrame({'Entry':randint(100000,999999),'ID':row['\ufeffID'], 'First Name': row['First name'], 'Last Name': row['Last name'], 'Program':gro_convert[i], 'Location':'East Van',
                                     'Status': 'Complete', 'Hours':hours_group[i], 'DateTime':date}, index=[0])
                lessons = pd.concat([lessons,line])

lessons.to_csv('lessons.csv', index=False)
