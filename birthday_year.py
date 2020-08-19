from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from abstract_API import AbstractAPI
import requests

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Shows all birthdays in a year!
class BirthdayYear (AbstractAPI):

    def __init__(self, arguments):
        super().__init__(arguments)

    def get_message(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API 

        year = datetime.datetime.utcnow().year # 'Z' indicates UTC time
        
        # lower and upper bounds
        firstday = str(year) + '-01-01T01:32:01.958954Z'
        lastday = str(year) + '-12-31T01:32:01.958954Z'
        
        # print('Procurando o proximo aniversario...')
        events_result = service.events().list(calendarId='c_s879dbc19c4ngj9huqjghritu4@group.calendar.google.com',
                                            singleEvents=True, maxResults=150, timeMin=firstday, timeMax=lastday, 
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        text = ''
        if not events:
            return 'No birthdays this year.'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date')) #date 
            text += '' + event['summary']  + ', dia ' + start +'\n'


        return text

