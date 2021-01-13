from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import path
import timestring
import datetime
import pickle
import os, os.path
import datetime

# directory & pathway setup
current_directory = os.getcwd()
target_directory = 'TideTimes(TEST)'
tide_times_directory = str(current_directory + '\\' + target_directory)

# if a token file containing the user's credentials already exists, then there is no need to recreate them
if path.exists("token.pkl"):

    # create a service object using the required service, its version and the credentials file
    service = build("calendar", "v3", credentials=pickle.load(open("token.pkl", "rb")))

    # create an object containing a list of calendars belonging to the user
    cl = service.calendarList().list().execute()

    # call a specific item from the first calendar called 'ID'
    calendar_id = cl['items'][0]['id']

    # Loop setup
    element_list = []

    end = 20

    # for every file inside the tide times directory
    for file in os.listdir(tide_times_directory):
        index = 0
        # if the file is a .csv, enter
        if (file.endswith('.csv')):
            # open the specific file in read mode
            with open(str(tide_times_directory + '\\' + file), 'r') as reader:
                # for each element inside the .csv
                for entry in reader:
                    if index == 0:      # this is to skip the column headings
                        index = 1
                        continue
                    # this is a testing condition so that it only makes X amount of entries, not the whole thing
                    if index == end:
                        break
                    else:
                        element_list = entry.split(',')
                        # do not add 'Low Water' elements, we are only interested in making events for 'High Water'
                        if element_list[3] == 'LW\n':
                            continue
                        else:
                            # Date
                            event_date = datetime.datetime.strptime(element_list[0], '%d-%m-%Y').strftime('%Y-%m-%d')

                            # Time
                            split_time = element_list[1].split(':')

                            tide_time = str(str(int(int(split_time[0]))).zfill(2) + ':' + split_time[1])
                            tide_time_end = str(str(int(int(split_time[0]) + 1)).zfill(2) + ':' + split_time[1])

                            session_time_start = str(str(int(int(split_time[0]) - 2)).zfill(2) + ':' + split_time[1])

                            minus_symbol = '-'

                            if minus_symbol in session_time_start:
                                session_time_start = tide_time

                            # Tide Height
                            event_height = element_list[2]

                            # Low or High Water
                            event_state = element_list[3]

                            first_part_start = tide_time.split(':')[0]
                            second_part_start = tide_time.split(':')[1]
                            first_part_end = tide_time_end.split(':')[0]
                            second_part_end = tide_time_end.split(':')[1]

                            if first_part_start == '24':
                                tide_time = str('23' + ':' + second_part_start)
                            if first_part_end == '24':
                                tide_time_end = str('23' + ':' + second_part_end)

                            tide_time_start = str(event_date + 'T' + tide_time + ':00' + '-00:00')
                            tide_time_end = str(event_date + 'T' + tide_time_end + ':00' + '-00:00')

                            event = {
                                'summary': str(event_state + ':' + tide_time + ' (' + session_time_start + ' start' + ') ' + event_height + 'm'),
                                'location': 'Gower, Swansea',
                                'description': 'Today\'s tide times',
                                'start': {
                                'dateTime': tide_time_start,
                                },
                                'end': {
                                'dateTime': tide_time_end,
                                },
                            }

                            event = service.events().insert(calendarId=calendar_id, body=event).execute()







# enter this block if this is the first time accessing the user's account
else:
    # If modifying these scopes, delete the file token.pickle.
    scopes = ['https://www.googleapis.com/auth/calendar']

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=scopes)
    credentials = flow.run_console()

    pickle.dump(credentials, open("token.pkl", 'wb'))



