# `stormbit.py`
Solution for the [weather-api](https://roadmap.sh/projects/weather-api-wrapper) challenge from [roadmap.sh](https://roadmap.sh).

A command-line weather application built in Python that fetches real-time weather data using the Visual Crossing API.  
Supports **current weather**, **hourly forecast**, **7-day forecast**, and **location handling** with a simple menu-based interface.

---

## How to run

Clone the repository and run:

```bash
git clone https://github.com/Abhinav08bhatt/stormbit.git
```
```bash
cd stormbit
```
```bash
python main.py
```

### Required module:
```bash
pip install requests
```

---

## Version Info:

<details><summary><strong>Version 1.0</strong> (latest)</summary>

### Features
- Current weather report  
- Hourly forecast for today  
- 7-day forecast  
- Location management:
  - Save a location  
  - Set default location  
  - View all saved locations  

### Supported actions (menu-based)
- Save a new location (`a`)
- View data of a saved location (`b`)
- Change default location (`c`)
- Present weather (`d`)
- Weather of whole day (`e`)
- Weather for next 7 days (`f`)

### Data Structure used in version 1.0

#### `saved_locations.json`
```json
{
    "default": "dehradun",
    "saved": ["mumbai","delhi"]
}
```

#### `cache.json`
Stores last successful response from the API.

</details>


---

## API Used
**Visual Crossing Weather API**  
(Free tier — requires an API key)

---

## License
This project is open-source and available under the MIT license.

