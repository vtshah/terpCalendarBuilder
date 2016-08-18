#scrape and generate JSON

import requests, json, datetime, time

courseName = 'CMSC131'
sectionID = '0502'

r = requests.get('http://api.umd.io/v0/courses/sections/' + courseName + '-' + sectionID)

#print(r.json())

instructors = r.json()['instructors'][0]
meetingsArr = r.json()['meetings']



def createEventJSON(instructors, meetingsArr):
    for x in meetingsArr:
        days = x['days']
        print(determine_start(days, x['start_time']))
        event = {
            'summary': courseName,
            'description': str('Taught By: ' + instructors + '. The class is located in ' + x['building'] + ' in room ' + x['room']),
            'location' : getLocation(x['building']),
            'start' : {
                'dateTime' : str(determine_start(days, x['start_time']).isoformat()),
                'timeZone' : 'America/New_York'
            },
            'end' : {
                'dateTime' : determine_end(days, x['end_time']),
                'timeZone' : 'America/New_York'
            },
            'recurrence' : [
                CreateRRuleString(findReccurences(days))
            ]
        }
        print(event)
    
def findReccurences(days):
    recurrArr = []
    if('M' in days):
        recurrArr.append('MO')
    if('Tu' in days):
        recurrArr.append('TU')
    if('W' in days):
        recurrArr.append('WE')
    if('Th' in days):
        recurrArr.append('TH')
    if('F' in days):
        recurrArr.append('FR')
    
    return recurrArr
    
def CreateRRuleString(recurrArr):
    rrule = "RRULE: FREQ=WEEKLY;BYDAY="
    for x in recurrArr:
        rrule = rrule + x + ','
    rrule = rrule[:-1]
    return rrule
    
    
def getLocation(building):
    b = requests.get('http://api.umd.io/v0/map/buildings/' + building)
    locationString = b.json()['lat'] + ', ' + b.json()['lng']
    print(locationString)
    return str(locationString)
    
    
def determine_start(days, timeStr):
    #startTime = datetime.datetime.strptime(datetime.datetime.fromtimestamp(time.mktime(time.strptime(timeStr, '%I:%M%p')), '%H:%M'))
    startTime = datetime.datetime.strptime(timeStr, '%I:%M%p').time()
    d = datetime.date(2016, 8, 29)
    arr = findReccurences(days)
    if(arr[0] == 'MO'):
        date = next_weekday(d, 0)
        return datetime.datetime.combine(date, startTime)
    elif(arr[0] == 'TU'):
        date = next_weekday(d, 1)
        return datetime.datetime.combine(date, startTime)
    elif(arr[0] == 'WE'):
        date = next_weekday(d, 2)
        return datetime.datetime.combine(date, startTime)
    elif(arr[0] == 'TH'):
        date = next_weekday(d, 3)
        return datetime.datetime.combine(date, startTime)
    elif(arr[0] == 'FR'):
        date = next_weekday(d, 4)
        return datetime.datetime.combine(date, startTime)
    else:
        return d;
        

def determine_end(days, timeStr):
    #startTime = datetime.datetime.strptime(datetime.datetime.fromtimestamp(time.mktime(time.strptime(timeStr, '%I:%M%p')), '%H:%M'))
    endTime = datetime.datetime.strptime(timeStr, '%I:%M%p').time()
    d = datetime.date(2016, 12, 12)
    arr = findReccurences(days)
    if(arr[-1] == 'MO'):
        date = last_weekday(d, 0)
        return datetime.datetime.combine(date, endTime)
    elif(arr[-1] == 'TU'):
        date = last_weekday(d, 1)
        return datetime.datetime.combine(date, endTime)
    elif(arr[-1] == 'WE'):
        date = last_weekday(d, 2)
        return datetime.datetime.combine(date, endTime)
    elif(arr[-1] == 'TH'):
        date = last_weekday(d, 3)
        return datetime.datetime.combine(date, endTime)
    elif(arr[-1] == 'FR'):
        date = last_weekday(d, 4)
        return datetime.datetime.combine(date, endTime)
    else:
        return d;
    
    

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def last_weekday(d, weekday):
    days_behind = weekday + d.weekday()
    if days_behind > 0: # Target day already happened this week
        days_behind -= 7
    return d + datetime.timedelta(days_behind)

       
createEventJSON(instructors, meetingsArr)

'''
event = {
  'summary': courseName,
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': '',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
'''
