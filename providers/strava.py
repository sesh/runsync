import os
import requests

from .base import Activity, BaseProvider

from stravalib.client import Client

STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
STRAVA_APP_ID = os.environ.get('STRAVA_APP_ID')

class StravaProvider(BaseProvider):

    provider = 'strava'

    def __init__(self, token):
        if not token:
            client = Client()
            url = client.authorization_url(client_id=STRAVA_APP_ID, redirect_uri='http://localhost:8000/')
            code = input(f"Open {url}, copy code once redirected: ")
            token_response = client.exchange_code_for_token(client_id=STRAVA_APP_ID, client_secret=STRAVA_CLIENT_SECRET, code=code)
            self.STRAVA_ACCESS_TOKEN = token_response['access_token']
        else:
            self.STRAVA_ACCESS_TOKEN = token

    def get_activities(self, skip_ids=[], limit=100):
        activities = []
        response = requests.get('https://www.strava.com/api/v3/athlete/activities?per_page=100', headers={
            'Authorization': 'Bearer {}'.format(self.STRAVA_ACCESS_TOKEN)
        })

        for activity in response.json()[:limit]:
            if activity['type'].lower() != 'run':
                print('Skipping non-running workout. {} ({})'.format(activity['id'], activity['type'].lower()))
                continue

            if activity['id'] in skip_ids:
                print('Skipping already synced workout. {}'.format(activity['id']))
                continue

            activity_streams = requests.get('https://www.strava.com/api/v3/activities/{}/streams/time,distance,altitude,latlng'.format(
                activity['id']
            ), headers={
                'Authorization': 'Bearer {}'.format(self.STRAVA_ACCESS_TOKEN)
            }).json()

            activity_obj = Activity(
                source_id=activity['id'],
                name=activity['name'],
                start=activity['start_date_local'],
                distance=activity['distance'] / 1000,
                duration=activity['elapsed_time'],
                provider='strava'
            )

            for stream in activity_streams:
                if stream['type'] == 'altitude':
                    activity_obj.elevation_values = stream['data']
                elif stream['type'] == 'time':
                    activity_obj.clock_values = stream['data']
                elif stream['type'] == 'distance':
                    activity_obj.distance_values = [x / 1000 for x in stream['data']]
                elif stream['type'] == 'latlng':
                    activity_obj.latitude_values = [x[0] for x in stream['data']]
                    activity_obj.longitude_values = [x[1] for x in stream['data']]

            activities.append(activity_obj)

        return activities
