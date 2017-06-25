`runsync` is a Python tool for suncing runs (and other activities) between services.

It currently supports exporting runs from [Strava][strava] to [Smashrun][smashrun].
I definitely intend on incorporating other services

---

## Usage

Install `requests` and run the tool on the command line:

```
export STRAVA_ACCESS_TOKEN='<strava-token>
export SMASHRUN_ACCESS_TOKEN='<smashrun-token>'
python runsync.py
```

(only tested with Python 3 - and tested with 3.6)

  [smashrun]: https://smashrun.com
  [strava]: https://strava.com
