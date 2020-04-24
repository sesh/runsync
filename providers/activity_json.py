import json
from math import radians, cos, sin, asin, sqrt

AVG_EARTH_RADIUS = 6371  # in km


def haversine(point1, point2, miles=False):
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers


class Activity:

    def __str__(self):
        return f"{self.name} {self.distance}km in {self.duration} ({self.provider} - {self.source_id})"

    def __init__(self, *, name, source_id, start, distance, duration, activity_type='running',
                 distance_values=[], longitude_values=[], latitude_values=[], elevation_values=[], clock_values=[],
                 heart_rate_values=[], external_id=None, provider=None, **kwargs):
        self.name = name
        self.source_id = source_id
        self.external_id = external_id  # id on another service
        self.start = start
        self.distance = distance  # in kms
        self.duration = duration
        self.activity_type = activity_type
        self.distance_values = distance_values  # in kms
        self.longitude_values = longitude_values
        self.latitude_values = latitude_values
        self.elevation_values = elevation_values  # in m
        self.clock_values = clock_values  # in s
        self.heart_rate_values = heart_rate_values
        self.provider = provider

    def json(self):
        data = {
            'properties': {
                'name': self.name,
                'source_id': self.source_id,
                'start': self.start,
                'distance': self.distance,
                'duration': self.duration,
                'activity_type': self.activity_type,
                'provider': self.provider,
            },
            'data': {
                'distance': self.distance_values,
                'longitude': self.longitude_values,
                'latitude': self.latitude_values,
                'elevation': self.elevation_values,
                'clock': self.clock_values,
                'heart_rate': self.heart_rate_values,
            }
        }
        return json.dumps(data, indent=2)

    @classmethod
    def load(cls, j):
        """
        Accepts a JSON string and returns an Activity object
        """
        activity_json = json.loads(j)
        kwargs = {}

        # explode the properties as kwargs
        kwargs.update(activity_json['properties'])

        # each key in data gets _values appended
        kwargs.update({k + '_values': v for k, v in activity_json['data'].items()})

        return Activity(**kwargs)

    def calculated_distance(self):
        distance = 0.0
        prev = None
        for point in zip(self.latitude_values, self.longitude_values):
            if prev:
                distance += haversine(point, prev)
            prev = point
        return distance

    def splits(self):
        splits = {}
        next_split = 1.0
        split_start = 0

        for i, distance in enumerate(self.distance_values):
            if distance >= next_split:
                splits[str(next_split)] =  self.clock_values[i] - split_start

                if distance == next_split:
                    split_start = self.clock_values[i]
                else:
                    split_start = self.clock_values[i-1]

                next_split += 1

        return splits
