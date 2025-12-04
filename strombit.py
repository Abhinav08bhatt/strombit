import os
import requests
import json
from time import sleep
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = ("BSYZABBSQMDYY5P3ZRC5SGVR2") # API = BSYZABBSQMDYY5P3ZRC5SGVR2

# ============================================== API SECTION ==============================================
def get_from_api(city):
    # Unit group metric ensures °C and % for humidity (if supported)
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_KEY}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()
# =========================================================================================================


# ============================================ DIAGNOSE-SECTION ===========================================
def write_in_file(data):
    data = get_from_api(city)
    with open("cache.json","w") as f:
        json.dump(data,f,indent=4)

def get_from_file():
    with open("cache.json","r") as f:
        data = json.load(f)
    return data

def pretty_print(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))
# =========================================================================================================

# ============================================= FORMAT-SECTION ============================================
def local_time(tz_name):
    local_time = datetime.now(ZoneInfo(tz_name))
    return local_time.strftime("%H:%M") # returns "14:32"

def hour_12(time):
    '''
    Convert 24-hour time to 12-hour format.
    
    :param time: string from local_time(), format "HH:MM"
    '''
    hour, minute = map(int, time.split(":"))

    period = "AM"
    if hour == 0:
        hour = 12
        period = "AM"
    elif hour == 12:
        period = "PM"
    elif hour > 12:
        hour -= 12
        period = "PM"

    return f"{hour:02d}:{minute:02d} {period}"


def date_formate(date):
    '''
    Convert yyyy-mm-dd → dd Month yyyy
    
    :param date: date from API (e.g., "2025-12-03")
    '''
    year, month, day = date.split("-")

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "June",
        "July", "Aug", "Sept", "Oct", "Nov", "Dec"
    ]

    month_name = months[int(month) - 1]

    return f"{day} {month_name} {year}"


def clear():
    '''
    to clear the terminal for a better console UI
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def style(s,n=0.04):
    '''
    nothing, just attention to details
    :param s: string input
    :param n: speed of text (default 0.04)
    '''
    
    for i in range (0,len(s)):
        print(s[i],end='')
        sleep(n)

def press_key():
    input("\n\nPress ENTER to continue...")

# =========================================================================================================

# ========================= IMPORTANT SECTION (could not think of better name) ============================

def read_locations(filename="saved_locations.json"):
    """
    Returns a dict with structure:
    {
        "default": str,
        "saved": [str, str, ...]
    }
    """
    if not os.path.exists(filename):
        # Initialize an empty structure if file doesn't exist
        return {"default": None, "saved": []}

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def write_locations(data, filename="saved_locations.json"):
    """
    Writes the dict back to disk.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def manage_locations(mode=1, new_name=None, filename="saved_locations.json"):
    """
    mode 1: return default name
    mode 2: add `new_name` to saved list
    mode 3: replace default with `new_name` and push old default into saved
    """
    data = read_locations(filename)

    if "default" not in data:
        data["default"] = None
    if "saved" not in data:
        data["saved"] = []

    # --- MODE 1: return default ---
    if mode == 1:
        return data["default"]

    # --- MODE 2: add to saved list ---
    elif mode == 2:
        if new_name is None:
            raise ValueError("mode 2 requires new_name")
        if new_name not in data["saved"]:
            data["saved"].append(new_name)
        write_locations(data, filename)
        return True

    # --- MODE 3: replace default ---
    elif mode == 3:
        if new_name is None:
            raise ValueError("mode 3 requires new_name")

        old_default = data["default"]

        if old_default is not None and old_default not in data["saved"]:
            data["saved"].append(old_default)

        data["default"] = new_name

        if new_name in data["saved"]:
            data["saved"].remove(new_name)

        write_locations(data, filename)
        return True

    else:
        raise ValueError("Invalid mode. Use 1, 2, or 3.")

def view_location(name=None, filename="saved_locations.json"):
    """
    Read-only viewer for saved location data.

    If name is None:
        returns the full dataset.
    If name is provided:
        returns:
            {"location": name, "type": "default"}
            {"location": name, "type": "saved"}
        or "Location does not exist" if not found.
    """

    data = read_locations(filename)

    # No name: return full data
    if name is None:
        return data

    # Match default
    if name == data.get("default"):
        return name
        # return {"location": name, "type": "default"}

    # Match saved list
    if name in data.get("saved", []):
        return name
        # return {"location": name, "type": "saved"}

    # Not found
    print("Location does not exist")
    ask = input(f"would you like to add {name} to saved location? [y/n] : ")
    if ask == "y":
        manage_locations(2,name)
        print(f"{name} added to saved location")
    return name

# ========================================== DATA-DELIVER SECTION =========================================
def currentTime_data(data):

    day_sameday_data = data["days"][0]
    date = day_sameday_data["datetime"]
    avg_temp = day_sameday_data["temp"]
    max_temp = day_sameday_data["tempmax"]
    min_temp = day_sameday_data["tempmin"]

    hour_sameday_data = data["days"][0]["hours"]
    current_time = local_time(data["timezone"])
    for i in hour_sameday_data:
        if i["datetime"][0:2] == current_time[0:2]:
                temp = i["temp"]
                feelslike = i["feelslike"]
                humidity = i["humidity"]
                conditions = i["conditions"]
                uvindex = i["uvindex"]
                visibility = i["visibility"]

    print(f'''
            Weather : {data["resolvedAddress"].capitalize()}
          
Time                        : {hour_12(local_time(data["timezone"]))}
Date                        : {date_formate(date)}

Current Temperature         : {temp}\u00B0C         
Feels like                  : {feelslike}\u00B0C

Max Temperature             : {max_temp}\u00B0C
Min Temperature             : {min_temp}\u00B0C
Average Temperature         : {avg_temp}\u00B0C
         
Humidity                    : {humidity}%
conditions                  : {conditions}
uvindex                     : {uvindex}
visibility                  : {visibility}
''')
    
def wholeDay_data(data):
    hour_sameday_data = data["days"][0]["hours"]

    print(f'''
            Hourly Forecast : {data["resolvedAddress"].capitalize()}
            Date            : {date_formate(data["days"][0]["datetime"])}
''')

    for hour in hour_sameday_data:
        temp = hour["temp"]
        feelslike = hour["feelslike"]
        precipprob = hour["precipprob"]
        windspeed = hour["windspeed"]
        uvindex = hour["uvindex"]
        cloudcover = hour["cloudcover"]

        print(f'''
Time                        : {hour_12(local_time(data["timezone"]))}

Temperature                 : {temp}°C
Feels like                  : {feelslike}°C

Rain Chance                 : {precipprob}%
Wind Speed                  : {windspeed} km/h
UV Index                    : {uvindex}
Cloud Cover                 : {cloudcover}%
''')

def next7Days_data(data):
    days_data = data["days"][:7]

    print(f'''
            Next 7 Days Forecast : {data["resolvedAddress"].capitalize()}
''')

    for d in days_data:
        date = d["datetime"]
        tempmax = d["tempmax"]
        tempmin = d["tempmin"]
        conditions = d["conditions"]
        precipprob = d["precipprob"]
        humidity = d["humidity"]
        windspeed = d["windspeed"]
        sunrise = d["sunrise"]
        sunset = d["sunset"]

        print(f'''
Date                       : {date_formate(date)}

High Temp                  : {tempmax}°C
Low Temp                   : {tempmin}°C

Conditions                 : {conditions}
Rain Chance                : {precipprob}%
Humidity                   : {humidity}%
Wind Speed                 : {windspeed} km/h

Sunrise                    : {sunrise}
Sunset                     : {sunset}
''')

# =========================================================================================================


# ================================================== main ==================================================
if __name__ == "__main__":
    
    clear()
    city = manage_locations() # default city
    if city is None:
        city = input("Enter your default city: ")
        manage_locations(3, city)

    try:
        data = get_from_api(city)
        # data = get_from_file()
        write_in_file(data)
    except requests.HTTPError as e:
        data = get_from_file()
        print("HTTP error:", e)
        try:
            print("Response text:", e.response.text)
        except Exception:
            pass
    except Exception as e:
        get_from_file()
        print("Error:", e)
    
    option = input('''
Enter the option from the menu : 

                LOCATION 
- save a new location               : a
- view data of a saved location     : b
- change default location           : c

        WEATHER (default location)
- view present weather              : d
- view the weather of whole day     : e
- view the weather for next 7 days  : f

- exit                              : x  
> ''')
    if option == "a":
        new_location = input("Enter the new location : ")
        manage_locations(2,new_location)
        print(f"{new_location} added to saved locations...")
    elif option == "b":
        locations = view_location()
        print(f"Default Location : {locations["default"].capitalize()}")
        print(f"Saved Locations : ")
        for i in locations["saved"]:
            print(f"                  {i.capitalize()}")
        ask = input("You want to know location of ? :")
        
        currentTime_data(get_from_api(view_location(ask)))
    elif option == "c":
        new_location = input("Enter the new DEFAULT location : ")
        manage_locations(3,new_location)
        print(f"{new_location} is now the default location...")
    elif option == "d":
        currentTime_data(data)
    elif option == "e":
        wholeDay_data(data)
    elif option == "f":
        wholeDay_data(data)
    elif option == "x":
        exit()
    else:
        print("Wrong Input")