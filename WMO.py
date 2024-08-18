from weatherBox import weatherBox
import pandas as pd
import re


class WMORow:
    def __init__(self, row: pd.DataFrame):
        self.row = row[4:]
        self.length: int = len(row) - 4
        self.code: str = str(row[1])
        self.calculation: str = str(row[2]).strip().lower()
        
    
    def isValid(self) -> bool:
        if self.length < 13:
            return False 

        codes = ['1', '2', '3', '4', '5', '8', '22', '23', '37', '38', '39']
        if self.code not in codes:
            return False

        calculations = ['count', 'count %', 'sum', 'mean', 'max', 'min']
        if self.calculation not in calculations:
            return False
        
        if (self.row.isnull().any()) :
            return False
        
        for num in self.row:
            try:
                float(num)
            except: 
                return False
        
        return True
    
    def toList(self) -> list[float]:
        data_list = []
        for data in self.row:
            data = float(data)
            data = round(data, 1)
            data_list.append(data)

        return data_list


def makeWeatherBox(url:str) -> str: 

    weather_box = weatherBox()

    codenames: dict[str, function] = {
        '1': weather_box.setPrecip,
        '2': weather_box.setPrecipDays,
        '3': weather_box.setMaxTemps,
        '4': weather_box.setMinTemps,
        '5': weather_box.setMeanTemps,
        '8': weather_box.setSunshine,
        '37': weather_box.setSnowfall,
        '38': weather_box.setHumidity,
        '39': weather_box.setDewPoint
    }

    climate_data = pd.read_csv(url)

    for index, row in climate_data.iterrows():
        if (row[0] == "Station_Name"):
            location = row[1]
        if len(row) >= 17:
            wmo_row: WMORow = WMORow(row)
            if wmo_row.isValid() and wmo_row.code in codenames:
                func = codenames[wmo_row.code]
                func(wmo_row.toList())

    
    location: str = location.title()
    weather_box.setHeader(location, "1991–2020")

    title:str = location + " Climate Normals for 1991-2020"
    weather_box.setFooter(url, title, agency="National Oceanic and Atmospheric Administration", format="CSV")

    return str(weather_box)


if __name__ == '__main__':
    url = input("URL: ")

    weather_box:str = makeWeatherBox(url)
    with open("weatherbox.txt", "w") as file:
        file.write(weather_box)
    
