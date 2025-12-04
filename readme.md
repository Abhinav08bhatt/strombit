# stormbit version 1.0 'strombit.py`

Solution for the [weather-api](https://roadmap.sh/projects/weather-api-wrapper-service) challenge from [roadmap.sh](https://roadmap.sh/).

## How to run

Clone the repository and run the following command:
```bash
git clone https://github.com/Abhinav08bhatt/stormbit.git
```
```bash
cd stormbit
```
```bash
python strombit.py
```

## Required module

```bash
pip install requests
```

## Supported Actions (menu-based)
- Save a new location (a)
- View weather of a saved location (b)
- Change default location (c)
- View present weather (d)
- View the weather of the whole day (e)
- View the weather for the next 7 days (f)

## Features in version 1.0
### Weather Data
- Current temperature, feels-like temperature
- Max / Min / Average temperature for the day
- Humidity, UV index, visibility
- Conditions (Clear, Cloudy, Rain, etc.)
### Today’s Hourly Forecast
- Temperature and feels-like
- Rain probability
- Wind speed
- UV index
- Cloud cover
### 7-Day Forecast
- Daily high and low
- Conditions
- Rain probability
- Humidity and wind speed
- Sunrise and sunset
### Location Management
- Default location support
- Save multiple locations
- View saved locations
- Query any saved location

## Data Structure used in version 1.0

`saved_locations.json`
```json
{
    "default": "dehradun",
    "saved": [
        "mumbai",
        "delhi"
    ]
}
```
`cache.json`
- Stores the last successful weather API response in case of errors.

## API Used

Weather data is fetched from Visual Crossing Weather API (Free tier, requires an API key)
in `strombit.py` line 8
```python
API_KEY = "YOUR API HERE"
```