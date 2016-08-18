from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime, requests, time, json

courseName = 'CMSC131'
sectionID = '0502'

r = requests.get('http://api.umd.io/v0/courses/sections/' + courseName + '-' + sectionID)

#print(r.json())

instructors = r.json()['instructors'][0]
meetingsArr = r.json()['meetings']


def createEventJSON(instructors, meetingsArr):
    events = []
    for x in meetingsArr:
        days = x['days']
        print(determine_start(days, x['start_time']))
	GMT_OFF = '-07:00'
        event = {
            'summary': courseName,
            'description': str('Taught By: ' + instructors + '. The class is located in ' + x['building'] + ' in room ' + x['room']),
            'location' : getLocation(x['building']),
            'start' : {
		'dateTime' : str(determine_start(days, x['start_time']).isoformat()),
		'timeZone' : 'America/New_York'
             },
            'end' : {
		'dateTime' : str(determine_end(days, x['end_time']).isoformat()),
		'timeZone' : 'America/New_York'
	     },
            'recurrence' : [
                CreateRRuleString(findReccurences(days))
            ]
        }
        events.append(event)
    return events
    
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



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

events = createEventJSON(instructors, meetingsArr)

e = CAL.events().insert(calendarId='primary',
        sendNotifications=True, body=events[0]).execute()

e = CAL.events().insert(calendarId='primary',
        sendNotifications=True, body=events[1]).execute()

print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'], e['end']['dateTime']))


