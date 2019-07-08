import base64
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


class Calendar:
    service_scopes = ['https://www.googleapis.com/auth/calendar']

    @staticmethod
    def _get_credentials():
        decode_token = json.loads(base64.b64decode(os.getenv('CALENDAR_TOKEN')).decode('utf-8'))
        credentials = service_account.Credentials.from_service_account_info(decode_token, scopes=Calendar.service_scopes)
        return credentials

    @staticmethod
    def create(name):
        credentials = Calendar._get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        calendar = service.calendars().insert(body={'summary': name}).execute()
        return calendar['id']

    @staticmethod
    def add_user(user_email, calendar_id):
        credentials = Calendar._get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        rule = {'scope': {'type': 'user', 'value': user_email}, 'role': 'reader'}
        return service.acl().insert(calendarId=calendar_id, body=rule).execute()

    @staticmethod
    def delete_user(user_email, calendar_id):
        credentials = Calendar._get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        rule = {'scope': {'type': 'user', 'value': user_email}, 'role': 'none'}
        return service.acl().insert(calendarId=calendar_id, body=rule).execute()

    @staticmethod
    def create_event(summary, description, start_date, end_date, calendar_email, attendees=None, reminders=None):
        credentials = Calendar._get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        event = {'summary': summary, 'description': description, 'start': {'date': start_date.strftime('%Y-%m-%d')},
                 'end': {'date': end_date.strftime('%Y-%m-%d')}, 'attendees': attendees, 'reminders': reminders}
        return service.events().insert(calendarId=calendar_email, body=event).execute()


