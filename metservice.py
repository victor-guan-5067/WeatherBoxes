from bs4 import BeautifulSoup
import requests
from weatherBox import weatherBox
    

def makeWeatherBox(parsed_page, url) -> str:

    tableSection = parsed_page.find("div", {"data-type":"Station", "data-period":"1991-2020"})
    title = parsed_page.find("title").text
    name = parsed_page.find("h2", {"class": "nearest-station-name"}).text
    table = tableSection.find("table")

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
                item = item[:-1]
                correct_list = param_indexes.get(i)
                correct_list.append(item)
            i += 1

    weather_box.setMaxTemps(max_temps)
    weather_box.setMinTemps(min_temps)
    weather_box.setSunshine(sunshine)
    weather_box.setRainfall(rainfall)
    weather_box.setRainDays(rain_days)
    
    weather_box.setFooter(url, title)

    return weather_box.getWeatherBox()


if __name__ == "__main__":
    url:str = input("Climate averages webpage: ")
    page = requests.get(url)
    bs = BeautifulSoup(page.content, "html.parser")
    weather_box:str = makeWeatherBox(bs, url)
    print(weather_box)
