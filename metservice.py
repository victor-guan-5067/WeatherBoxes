from bs4 import BeautifulSoup
import requests
from weatherBox import weatherBox
    

def makeWeatherBox(parsed_page, url) -> str:

    title = parsed_page.find("title").text
    name = parsed_page.find("h2", {"class": "nearest-station-name"}).text
    name = name.split('-')[0]
    table_section = parsed_page.find("div", {"data-type":"Station", "data-period":"1991-2020"})
    table = table_section.find("table")

    weather_box = weatherBox()

    weather_box.setHeader(name)

    max_temps: list = []
    min_temps: list = []
    sunshine: list = []
    rainfall: list = []
    rain_days: list = []

    param_indexes = {1: max_temps, 2: min_temps, 4: sunshine, 5: rainfall, 6: rain_days}

    rows = table.find("tbody")
    for row in rows:
        items = row.text.split()
        i = 0
        for item in items:
            if i in param_indexes and item != '–':
                rounded_val = round(float(item), 1)
                correct_list = param_indexes.get(i)
                correct_list.append(rounded_val)
            i += 1

    if len(max_temps) == 13:
        weather_box.setMaxTemps(max_temps)
    if len(min_temps) == 13:
        weather_box.setMinTemps(min_temps)
    if len(sunshine) == 13:
        weather_box.setSunshine(sunshine)
    if len(rainfall) == 13:
        weather_box.setRainfall(rainfall)
    if len(rain_days) == 13:
        weather_box.setRainDays(rain_days, "1 mm")
    
    weather_box.setFooter(url, title, "Met Office")

    return str(weather_box)


if __name__ == "__main__":
    url:str = input("Climate averages webpage: ")
    page = requests.get(url)
    bs = BeautifulSoup(page.content, "html.parser")
    weather_box:str = makeWeatherBox(bs, url)
    with open("weatherbox.txt", "w") as file:
        file.write(weather_box)
