import os
import requests

from .base import BaseProvider


SMASHRUN_ACCESS_TOKEN = os.environ.get('SMASHRUN_ACCESS_TOKEN')


class SmashrunProvider(BaseProvider):

    def add_activity(self, activity):
        data = {
            'startDateTimeLocal': activity.start.replace('17:21:00', '17:25:00'),
            'distance': activity.distance,
            'duration': activity.duration,
            'activityType': activity.activity_type,

            'recordingKeys': [
                k for k in ['clock', 'distance', 'longitude', 'latitude', 'elevation']
                if getattr(activity, '{}_values'.format(k))
            ],
            'recordingValues': [
                getattr(activity, '{}_values'.format(k))
                for k in ['clock', 'distance', 'longitude', 'latitude', 'elevation']
                if getattr(activity, '{}_values'.format(k))
            ],

        }

        response = requests.post('https://api.smashrun.com/v1/my/activities/', json=data, headers={
            'Authorization': 'Bearer {}'.format(SMASHRUN_ACCESS_TOKEN)
        }).json()

        if 'validations' in response:
            for v in response['validations']:
                print('Uploaded failed! {} - {}'.format(v, ' '.join(response['validations'][v])))
