import requests
from requests.adapters import Retry
from weatherBox import weatherBox
import json
import time
from pathlib import Path
    

def makeWeatherBox(data: json, webpage_url: str) -> str:
    title = "World Weather Information Service"

    city_data = data["city"]
    city_name = city_data["cityName"]
    climate = city_data["climate"]

    # return nothing if there is no rain type
    if (climate["raintype"] == "N/A"):
        return ""

    start_year = climate["datab"]
    end_year = climate["datae"]
    years: str = str(start_year) + '–' + str(end_year)

    weather_box = weatherBox()

    weather_box.setHeader(city_name, years)

    rain_amount = climate["raindef"]
    rain_unit = climate["rainunit"]
    if (rain_amount != '' and rain_unit != ''):
        precip_threshold: str = climate["raindef"] + ' ' + climate["rainunit"]
    else:
        precip_threshold = None

    max_temps: list = []
    min_temps: list = []
    rainfall: list = []
    rain_days: list = []

    for month in climate["climateMonth"]:
        if (month["maxTemp"] != (None or "")):  
            max_temps.append(month["maxTemp"])
        if (month["minTemp"] != (None or "")):
            min_temps.append(month["minTemp"])
        if (month["rainfall"] != (None or "")):
            rainfall.append(month["rainfall"])
        if (month["raindays"] != (None or "")):
            rain_days.append(month["raindays"])
    
    if (len(max_temps) >= 12):
        weather_box.setMaxTemps(max_temps)
    if (len(min_temps) >= 12):
        weather_box.setMinTemps(min_temps)

    raintype:str = climate["raintype"]

    if (raintype == "PPT"):
        if (len(rainfall) >= 12):
            weather_box.setPrecip(rainfall)
        if (len(rain_days) >= 12):
            weather_box.setPrecipDays(rain_days, precip_threshold)
    elif (raintype == "Rainfall"):
        if (len(rainfall) >= 12):
            weather_box.setRainfall(rainfall)
        if (len(rain_days) >= 12):
            weather_box.setRainDays(rain_days, precip_threshold)
    
    weather_box.setFooter(webpage_url, title, "World Meteorological Organization")

    return str(weather_box)


def write_weather_box(weather_box: str):
    '''
        Writes weather box and creates a file.
    '''
    # Get the user's home directory
    home_dir = Path.home()

    # Define the path for the new folder in the Documents directory
    documents_dir = home_dir / "Documents" / "WMO website weatherboxes"
    country_dir: Path = documents_dir / country
    country_dir.mkdir(exist_ok=True)

    city_file: Path = country_dir / f"{city}.txt"
    try:
        city_file.touch(exist_ok=True)
    except:
        print(f"Failed to make file for {city}, {country}")
    city_file.write_text(weather_box)


if __name__ == "__main__":
    i: int = 4000
    while (i < 10000):
        webpage_url = "https://worldweather.wmo.int/en/city.html?cityId={}".format(i)
        xml_url = "https://worldweather.wmo.int/en/json/{}_en.xml".format(i)
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504 ])
        xml_request = s.get(xml_url)
    
        if (xml_request.status_code == 200): 

            # skip everything if the xml request has no text (i.e. xml exists but has no content)
            if (xml_request.text == ""):
                i += 1
                continue

            # NOTE: DO NOT REMOVE 
            # Waits 5 seconds to scrape page to avoid overloading
            time.sleep(5)       
            xml = json.loads(xml_request.text)

            country: str = xml["city"]["member"]["memName"]
            city: str = xml["city"]["cityName"]
            city = city.replace("/", "-")

            try:
                weather_box:str = makeWeatherBox(xml, webpage_url)
            except:
                print(f"Making weather box failed for {city}, {country}")

            # skip iteration if no climate data
            if (weather_box != ""):
                print(f"city {i}: {city}, {country}")
                write_weather_box(weather_box)
    
        i += 1

    '''
    webpage_url: str = input("Enter climate averages webpage: ")
    city_id: str = webpage_url.split("cityId=")[1]
    xml_url = "https://worldweather.wmo.int/en/json/{}_en.xml".format(city_id)
    xml_request = requests.get(xml_url)
    
    if (xml_request.status_code == 200):        
        xml = json.loads(xml_request.text)
        weather_box:str = makeWeatherBox(xml, webpage_url)
        with open("weatherbox.txt", "w") as file:
            file.write(weather_box)
    '''