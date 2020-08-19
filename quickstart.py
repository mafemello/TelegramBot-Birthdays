from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
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

    
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    
    print ('sera que tem aniversario hoje?')
    events_result = service.events().list(calendarId='c_s879dbc19c4ngj9huqjghritu4@group.calendar.google.com',
                                        singleEvents=True, maxResults=1, timeMin=now, 
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Nao tem aniversario hoje.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print('Feliz aniversário,', event['summary'], 'que as arestas estejam com você.')


if __name__ == '__main__':
    main()
