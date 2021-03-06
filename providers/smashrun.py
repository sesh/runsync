import os
import requests

from .base import Activity, BaseProvider


SMASHRUN_ACCESS_TOKEN = os.environ.get('SMASHRUN_ACCESS_TOKEN')


class SmashrunProvider(BaseProvider):

    def __init__(self, token=None):
        if not token:
            raise Exception("Smashrun token required, created one with the API Explorer: https://api.smashrun.com/explorer")
        self.SMASHRUN_ACCESS_TOKEN = token

    def get_activity_external_ids(self):
        activities = []
        response = requests.get('https://api.smashrun.com/v1/my/activities', headers={
            'Authorization': 'Bearer {}'.format(self.SMASHRUN_ACCESS_TOKEN)
        })

        for activity in response.json():
            activities.append(activity['externalId'])

        return activities

    def get_activities(self, limit=10):
        activities = []
        response = requests.get('https://api.smashrun.com/v1/my/activities', headers={
            'Authorization': 'Bearer {}'.format(self.SMASHRUN_ACCESS_TOKEN)
        })

        for activity in response.json()[:limit]:
            if activity['activityType'].lower() != 'running':
                print('Skipping non-running workout.')
                continue

            activity_detail = requests.get('https://api.smashrun.com/v1/my/activities/' + str(activity['activityId']), headers={
                'Authorization': 'Bearer {}'.format(self.SMASHRUN_ACCESS_TOKEN)
            }).json()

            activity_obj = Activity(
                name=activity['notes'],
                start=activity['startDateTimeLocal'],
                distance=activity['distance'] * 1000,
                duration=activity['duration'],
                external_id=activity['externalId'],
                source_id=activity['activityId'],
            )

            for stream in ['altitude', 'clock', 'distance', 'longitude', 'latitude']:
                if stream in activity_detail['recordingKeys']:
                    setattr(activity_obj, '{}_values'.format(stream), activity_detail['recordingValues'][activity_detail['recordingKeys'].index(stream)])  # noqa
            activities.append(activity_obj)

        return activities

    def add_activity(self, activity):
        data = {
            'startDateTimeLocal': activity.start.replace('17:21:00', '17:25:00'),
            'distance': activity.distance,
            'duration': activity.duration,
            'activityType': activity.activity_type,
            'externalId': activity.external_id if activity.external_id else '',

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
            'Authorization': 'Bearer {}'.format(self.SMASHRUN_ACCESS_TOKEN)
        }).json()

        if 'validations' in response:
            for v in response['validations']:
                print('Uploaded failed! {} - {}'.format(v, ' '.join(response['validations'][v])))
