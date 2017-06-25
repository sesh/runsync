

class BaseProvider:

    def get_activities(self):
        raise NotImplementedError

    def add_activity(self, gpx_file):
        raise NotImplementedError


class Activity:

    def __str__(self):
        return self.name

    def __init__(self, *, name, start, distance, duration, activity_type='running',
                 distance_values=[], longitude_values=[], latitude_values=[], elevation_values=[], clock_values=[]):
        self.name = name
        self.start = start
        self.distance = distance
        self.duration = duration
        self.activity_type = activity_type
        self.distance_values = distance_values
        self.longitude_values = longitude_values
        self.latitude_values = latitude_values
        self.elevation_values = elevation_values
        self.clock_values = clock_values
