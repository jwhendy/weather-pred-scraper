### Introduction

During some work on my garage roof ~1yr ago (2015), I found myself depending on weather forecasts far more than usual, as I needed to drag a tarp onto my bare roof in case it rained. I've never been very obsessed with weather forecasts in the past, but during this period of time it really mattered to me! I was somewhat shocked at how bad the predictions seemed to be. I'd check for the night and find it should be clear, suddenly to start seeing sprinkles right before I was haeding off to bed. I'd scramble outside and lug this enormous tarp over the garage. Other times the forecast would say it was going to rain, I'd drag the tarp up there, and nothing would happen.

I also looked into the sort of week I was going to have... would I have a solid 3+ days of no rain so I could count on a lot of work, or was it going to be intermittently raining all week and I wouldn't get much done?

In any case, I became interested in how predictions change as the day approaches. Basically, for any time (like now), what did the forecast say now's conditions would be 1hr, 3hrs, 2days, or a week ago?

I had recently completed the free `python` classes in the [Python for Everybody](https://www.coursera.org/specializations/python) series on Coursera (Dr. Charles Severence), and thought this would be a great opportunity to get my feet wet. I found some APIs and wrote a python script for each. I used a Raspberry Pi to collect hourly predictions for the next 48hrs, every hour. In other words, if I ran it right now, I'd get 48 predictions back, one for each hour in the next two ays. This was mainly due to the convenience of 48hr calls existing for each API.

I included a presentation (`weather-pred.pdf`) given at [pymntos](http://www.meetup.com/PyMNtos-Twin-Cities-Python-User-Group/) and [tcrug](http://www.meetup.com/twincitiesrug/) so you can learn more about my "trial run" and see some of the plots from sample data. My future plan is to refine the code and run it for more cities/climates as well as to grab data from a wider time frame (maybe rolling hourly or half-day predictions for a whole 7-10 days).

I make no promises about the code... this was written at a stage when I was barely above noob status, and that's still about where I am.


### Usage

To get setup, you'll need to populate a directory with API keys (see references section below). Aeris requires an id and secret, and Forecast.io and Weather Underground just require a key. On my system, the structure is like so:

```
[weather-pred-scraper] $ tree ./api_keys
├── aeris_api_id
├── aeris_api_secret
├── forecast_api_key
└── wunder_api_key
```

This directory structure/file names are used in each script to pull your key value in. Change each source file if you prefer a different naming/storage convention.

There are three scripts, located in `./src`. I've tried to make this reproducible by using the `os.getcwd()` command. On my system, I change into the repo directory, and then run the desired script. Example:

```
cd /path/to/weather-pred-scraper
python2 ./src/forecast.py
```

That will dump a `.json` and `.csv` file into the top directory.

For my trial run, I had a `./data` directory, and adjusted the script on the RPi to write them in there vs. cluttering the top level directory. At that point, I simply setup three cron jobs:

```
0 * * * * /path/to/weather-pred-scraper/src/aeris.py
0 * * * * /path/to/weather-pred-scraper/src/forecast.py
0 * * * * /path/to/weather-pred-scraper/src/wunder.py
```

This will run each script at the top of the hour.

I included three files, `fiddle_*` so you can see an example of the `.csv` output.

### References

*API keys*
- [Aeris](http://www.aerisweather.com/support/docs/api/)
- [forecast.io](https://developer.forecast.io/)
- [Weather Underground](https://www.wunderground.com/weather/api/)
