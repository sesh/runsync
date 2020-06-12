`runsync` is a Python tool for syncing runs (and other activities) between services.

It currently supports exporting runs from [Strava][strava] to [Smashrun][smashrun].
I definitely intend on incorporating other services.

_This is a WIP. I recommend looking at `runsync.py` and having a play around._

---

## Usage

You need to gather and export three environment variables:

- SMASHRUN_TOKEN - obtainable from the [Smashrun API Explorer][sr-api]
- STRAVA_APP_ID and STRAVA_CLIENT_SECRET - create an app in your [Strava API Settings][strava-api]

When you run you will be asked to open a URL to perform the Strava OAuth handshake. This is required because the access token that Strava provides in your profile does not have permission to read activities (at least for me).

Once you have the environment variables configured you can run with:

```bash
> pipenv run python runsync.py
```

This will attempt to sync the 100 most recent activities between the two services.


  [smashrun]: https://smashrun.com
  [strava]: https://strava.com
  [sr-api]: https://api.smashrun.com/explorer
  [strava-api]: https://www.strava.com/settings/api
