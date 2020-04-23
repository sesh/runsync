from .activity_json import Activity  # noqa


class BaseProvider:

    def get_activities(self):
        raise NotImplementedError

    def add_activity(self, gpx_file):
        raise NotImplementedError

