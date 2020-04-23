from .base import BaseProvider


class FileSystemProvider(BaseProvider):

    def get_activities(self, limit=10):
        return []

    def add_activity(self, activity):
        with open(f'{activity.source_id}.json', 'w') as f:
            f.write(activity.json())
