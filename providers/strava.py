import os
import requests

from .base import Activity, BaseProvider


STRAVA_ACCESS_TOKEN = os.environ.get('STRAVA_ACCESS_TOKEN')


class StravaProvider(BaseProvider):

    def get_activities(self, limit=1):
        activities = []
        response = requests.get('https://www.strava.com/api/v3/athlete/activities', headers={
            'Authorization': 'Bearer {}'.format(STRAVA_ACCESS_TOKEN)
        })

        for activity in response.json()[:limit]:
            if activity['type'].lower() != 'run':
                print('Skipping non-running workout.')
                continue

            activity_streams = requests.get('https://www.strava.com/api/v3/activities/{}/streams/time,distance,altitude,latlng'.format(
                activity['id']
            ), headers={
                'Authorization': 'Bearer {}'.format(STRAVA_ACCESS_TOKEN)
            }).json()

            activity_obj = Activity(
                name=activity['name'],
                start=activity['start_date_local'],
                distance=activity['distance'] / 1000,
                duration=activity['elapsed_time']
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
