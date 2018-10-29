from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime(2016,1,10).isoformat() + 'Z'  # Z indicates utc time
    print('Getting all events from {}'.format(now))
    events_result = service.events().list(calendarId='j10fjtc5p1dgvl0di9haf0fo80@group.calendar.google.com', timeMin=now,
                                          maxResults=10000000, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    folgas_oda = []
    servicos_oda = []
    for event in events:
        desc = event['summary']
        if 'DS' in desc:
            if 'ODA' in desc and 'Folga' not in desc and 'folga' not in desc and 'FOLGA' not in desc:
                servicos_oda.append(event)
            if 'ODA' in desc and ('Folga' in desc or 'folga' in desc or 'FOLGA' in desc):
                folgas_oda.append(event)
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    print('numero servicos ODA: {}'.format(len(servicos_oda)))
    print('numero folgas ODA: {}'.format(len(folgas_oda)))
    print('servicos\t\t\tfolgas')
    rows = max(len(servicos_oda),len(folgas_oda))
    for i in range(rows):
        if i < len(servicos_oda):
            s_start = servicos_oda[i]['start'].get('dateTime', servicos_oda[i]['start'].get('date'))
            print('{} - {}\t\t'.format(s_start, servicos_oda[i]['summary']), end='')
        if i < len(folgas_oda):
            f_start = folgas_oda[i]['start'].get('dateTime', folgas_oda[i]['start'].get('date'))
            print('{} - {}'.format(f_start, folgas_oda[i]['summary']))
        else:
            print('')


    print('{} folgas por gozar'.format(len(servicos_oda) - len(folgas_oda)))

if __name__ == '__main__':
    main()
