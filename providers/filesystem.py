from .base import BaseProvider, Activity

from os import listdir
from os.path import isfile, join

import json


class FileSystemProvider(BaseProvider):

    def __init__(self, prefix):
        self.prefix = prefix

    def get_activities(self):
        jsonfiles = [f for f in sorted(listdir(self.prefix)) if isfile(join(self.prefix, f)) and f.endswith('.json')]
        activities = []

        for fn in jsonfiles:
            with open(self.prefix + fn, 'r') as f:
                activities.append(Activity.load(f.read()))

        return activities

    def add_activity(self, activity):
        with open(f'{self.prefix}{activity.provider}-{activity.source_id}.json', 'w') as f:
            f.write(activity.json())
