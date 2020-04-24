from providers.strava import StravaProvider
from providers.filesystem import FileSystemProvider
from providers.smashrun import SmashrunProvider

import os


def format_mins_seconds(d):
    minutes, seconds = divmod(d, 60)
    return f"{minutes:02}:{seconds:02}"


def sync_strava_to_smashrun(sp, sr):
    sr_ids = sr.get_activity_external_ids()
    activities = sp.get_activities(skip_ids=sr_ids)

    for a in activities:
        sr.add_activity(a)


def print_split(activities):
    splits = []
    splits_2k = []
    splits_5k = []
    splits_10k = []

    for a in activities:
        s = [x for x in a.splits().values()]
        splits.extend(s)

        if len(s) >= 2:
            splits_2k.extend([sum(s[i:i+2]) for i in range(len(s)-1)])

        if len(s) >= 5:
            splits_5k.extend([sum(s[i:i+5]) for i in range(len(s)-4)])
        
        if len(s) >= 10:
            splits_10k.extend([sum(s[i:i+10]) for i in range(len(s)-9)])

    print("1K:", format_mins_seconds(min(splits)))
    print("2K:", format_mins_seconds(int(min(splits_2k))))
    print("5K:", format_mins_seconds(int(min(splits_5k))))
    print("10K:", format_mins_seconds(int(min(splits_10k))))


if __name__ == '__main__':
    sp = StravaProvider(token=None)
    fs = FileSystemProvider(prefix='./runs/')
    sr = SmashrunProvider(token=os.environ.get('SMASHRUN_TOKEN'))

    activities = fs.get_activities()

    for a in activities:
        sr.add_activity(a)