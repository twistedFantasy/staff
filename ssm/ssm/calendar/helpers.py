import argparse
import base64
import datetime
import pickle
import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.pickle.
STAFF_SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/admin.directory.group']
SERVICE_SCOPES = ['https://www.googleapis.com/auth/calendar']
token_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tokens')
STAFF_ACCOUNT_FILE = os.path.join(token_dir, 'token.pickle')
SERVICE_ACCOUNT_FILE = os.path.join(token_dir, 'token_sa.json')
OAUTH_FILE = os.path.join(token_dir, 'client_secret.json')


def get_staff_creds():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(STAFF_ACCOUNT_FILE):
        with open(STAFF_ACCOUNT_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_FILE, STAFF_SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(STAFF_ACCOUNT_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SERVICE_SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_iam_service():
    creds = get_staff_creds()
    service = build('iam', 'v1', credentials=creds)
    return service


def get_or_create_service_account():
    """Creates a service account."""
    name = 'staffy-service-account'
    display_name = 'staffy-service-account'
    with open(OAUTH_FILE, 'r') as f:
        project_id = json.load(f)['installed']['project_id']
    email = '%s@%s.iam.gserviceaccount.com' % (name, project_id)
    service = get_iam_service()
    try:
        service_account = service.projects().serviceAccounts().create(
            name='projects/' + project_id,
            body={
                'accountId': name,
                'serviceAccount': {
                    'displayName': display_name
                }
            }).execute()
    except HttpError as e:
        if e.resp.status == 409:
            service_account = service.projects().serviceAccounts().get(name='projects/%s/serviceAccounts/%s'
                                                                            % (project_id, email)).execute()
        else:
            raise e
    print('Service account: ' + service_account['email'])
    return service_account


def create_service_account_key():
    """Creates a key for a service account."""
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        return
    print('Create new service account key')
    account = get_or_create_service_account()
    email, id = account['email'], account['uniqueId']
    service = get_iam_service()
    key = service.projects().serviceAccounts().keys().create(name='projects/-/serviceAccounts/%s' % email,
                                                             body={'privateKeyType': 'TYPE_GOOGLE_CREDENTIALS_FILE'})\
        .execute()
    json_str = base64.b64decode(key['privateKeyData']).decode('utf-8')
    sa_key = json.loads(json_str)
    with open(SERVICE_ACCOUNT_FILE, 'w') as f:
        json.dump(sa_key, f)


def create_calendar(name):
    print('Create calendar with name %s' % str(name))
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SERVICE_SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    calendar = service.calendars().insert(body={'summary': name}).execute()
    return calendar['id']


def add_user_to_calendar(user_email, calendar_email):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SERVICE_SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    rule = {
        'scope': {
            'type': 'user',
            'value': user_email,
        },
        'role': 'reader'
    }
    service.acl().insert(calendarId=calendar_email, body=rule).execute()


def create_tokens():
    get_staff_creds()
    get_or_create_service_account()
    create_service_account_key()


def init_calendar(name):
    create_tokens()
    calendar_id = create_calendar(name)
    dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir, 'calendar_settings.py'), 'w') as f:
        f.write('CALENDAR_EMAIL = \'%s\'' % str(calendar_id))


def add_event_to_calendar(summary, description, start_date, end_date, calendar_email):
    print(summary, description, start_date, end_date, calendar_email)
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'date': start_date.strftime('%Y-%m-%d'),
        },
        'end': {
            'date': end_date.strftime('%Y-%m-%d')
        }
        # ,
        # 'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        # ],
        # 'reminders': {
        #     'useDefault': False,
        #     'overrides': [
        #         {'method': 'email', 'minutes': 24 * 60},
        #         {'method': 'popup', 'minutes': 10},
        #     ],
        # },
    }
    event = service.events().insert(calendarId=calendar_email, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def delete_calendars():
    page_token = None
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SERVICE_SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        service.calendarList().delete(calendarId=calendar_list_entry['id']).execute()


def get_calendars():
    page_token = None
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SERVICE_SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        print(calendar_list_entry['id'])


def create_group():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                                                  scopes=[
                                                                      'https://www.googleapis.com/auth/admin.directory.group'])
    service = build('admin', 'directory_v1', credentials=creds)
    email = creds.signer_email
    group = service.groups().insert(body={
        "email": "sales_group@codex-soft.com",
        "name": "Sales Group",
        "description": "This is the Sales group."
    }).execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create google calendar for organization')
    parser.add_argument('--create-tokens', dest='create_tokens', action='store_true', help='create service account '
                                                                                           'key')
    parser.add_argument('--init-calendar', dest='init_calendar', type=str, help='name of the calendar')
    args = parser.parse_args()
    if args.create_tokens:
        create_tokens()
    elif args.init_calendar:
        init_calendar(args.init_calendar)
    else:
        raise BaseException('Wrong parameter! Use -h')
