from providers.strava import StravaProvider
from providers.smashrun import SmashrunProvider


if __name__ == '__main__':
    sp = StravaProvider()
    sr = SmashrunProvider()
    activities = sp.get_activities()
    for a in activities:
        sr.add_activity(a)

