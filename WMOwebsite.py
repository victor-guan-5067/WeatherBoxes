import requests
from weatherBox import weatherBox
import json
    

def makeWeatherBox(data: json, webpage_url: str) -> str:
    title = "World Weather Information Service"

    city_data = data["city"]
    city_name = city_data["cityName"]
    climate = city_data["climate"]

    start_year = climate["datab"]
    end_year = climate["datae"]
    years: str = str(start_year) + '–' + str(end_year)

    weather_box = weatherBox()

    weather_box.setHeader(city_name, years)

    precip_threshold: str = climate["raindef"] + ' ' + climate["rainunit"]

    max_temps: list = []
    min_temps: list = []
    rainfall: list = []
    rain_days: list = []

    for month in climate["climateMonth"]:
        max_temps.append(month["maxTemp"])
        min_temps.append(month["minTemp"])
        rainfall.append(month["rainfall"])
        rain_days.append(month["raindays"])
    
    weather_box.setMaxTemps(max_temps)
    weather_box.setMinTemps(min_temps)

    raintype:str = climate["raintype"]

    if (raintype == "PPT"):
        weather_box.setPrecip(rainfall)
        weather_box.setPrecipDays(rain_days, precip_threshold)
    elif (raintype == "Rainfall"):
        weather_box.setRainfall(rainfall)
        weather_box.setRainDays(rain_days, precip_threshold)
    
    weather_box.setFooter(webpage_url, title, "World Meteorological Organization")

    return str(weather_box)


if __name__ == "__main__":
    webpage_url: str = input("Enter climate averages webpage: ")
    city_id: str = webpage_url.split("cityId=")[1]
    xml_url = "https://worldweather.wmo.int/en/json/{}_en.xml".format(city_id)
    xml_request = requests.get(xml_url)
    
    if (xml_request.status_code == 200):        
        xml = json.loads(xml_request.text)
        weather_box:str = makeWeatherBox(xml, webpage_url)
        with open("weatherbox.txt", "w") as file:
            file.write(weather_box)
