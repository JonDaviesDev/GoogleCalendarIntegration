from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import path
import datetime
import pickle
import os, os.path
import datetime

current_directory = os.getcwd()
target_directory = 'TideTimes'
tide_times_directory = str(current_directory + '\\' + target_directory)

# if a token file containing the user's credentials already exists, then there is no need to recreate them
if path.exists("token.pkl"):

    # create a service object using the required service, its version and the credentials file
    service = build("calendar", "v3", credentials=pickle.load(open("token.pkl", "rb")))

    cl = service.calendarList().list().execute()

    calendar_id = cl['items'][0]['id']

    element_list = []
    index = 0
    end = 7

    for file in os.listdir(tide_times_directory):
        if (file.endswith('.csv')):
            with open(str(tide_times_directory + '\\' + file), 'r') as reader:
                for entry in reader:
                    if index == 0:      # this is to skip the column headings
                        index = 1
                        continue
                    if index == end:
                        break
                    else:
                        element_list = entry.split(',')
                        event_date = datetime.datetime.strptime(element_list[0], '%d-%m-%Y').strftime('%Y/%m/%d')
                        split_time = element_list[1].split(':')
                        event_time = str(str(int(int(split_time[0]) - 2)) + ':' + split_time[1])
                        event_height = element_list[2]
                        event_state = element_list[3]

                        event = {
                            'summary': str(event_state + ': ' + event_time + ' - ' + event_height + 'm'),
                            'location': 'Gower, Swansea',
                            'description': 'Today\'s tide times',
                            'start': {
                            'dateTime': '2020-12-29T09:00:00-07:00',
                            'timeZone': 'Europe/London',
                            },
                            'end': {
                            'dateTime': '2020-12-29T17:00:00-07:00',
                            'timeZone': 'Europe/London',
                            }
                        }

                        event = service.events().insert(calendarId=calendar_id, body=event).execute()







# enter this block if this is the first time accessing the user's account
else:
    # If modifying these scopes, delete the file token.pickle.
    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=scopes)
    credentials = flow.run_console()

    pickle.dump(credentials, open("token.pkl", 'wb'))



