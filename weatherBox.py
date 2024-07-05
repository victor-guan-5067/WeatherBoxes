from datetime import date


class weatherBox:

    months: dict[int, str] = {
        0: "Jan",
        1: "Feb",
        2: "Mar",
        3: "Apr",
        4: "May",
        5: "Jun",
        6: "Jul",
        7: "Aug",
        8: "Sep",
        9: "Oct",
        10: "Nov",
        11: "Dec",
        12: "year"
    }

    def __init__(self):
        self.header:str = ""
        self.max_temps:str = ""
        self.min_temps:str = ""
        self.rainfall:str = " | rain colour = green\n"
        self.rain_days:str = " | unit rain days = 0.01 mm\n"
        self.sunshine:str = ""
        self.footer:str = ""

    def setHeader(self, location:str):
        header = '''
{{{{Weather box
 | width       = auto
 | metric first = yes
 | single line = yes
 | location    = {} (1991–2020)
'''
        self.header = header.format(location)

    def testLength(self, items:list, item_name:str):
        if len(items) != 13:
            raise ValueError("{} does not have 13 values (12 months plus year value).".format(item_name))
        
    def createRows(self, items: list, row_text: str):
        rows = ""
        i = 0
        for item in items:
            rows += " | {} {} = {}\n".format(self.months.get(i), row_text, item)
            i += 1
        return rows

    def setMaxTemps(self, max_temps_list:list):
        self.testLength(max_temps_list, "Max temps")
        self.max_temps += self.createRows(max_temps_list, "high C")

    def setMinTemps(self, min_temps_list:list):
        self.testLength(min_temps_list, "Min temps")
        self.min_temps += self.createRows(min_temps_list, "low C")

    def setRainfall(self, rainfall_list:list):
        self.testLength(rainfall_list, "Rainfall")
        self.rainfall += self.createRows(rainfall_list, "rain mm")

    def setRainDays(self, rain_days_list:list):
        self.testLength(rain_days_list, "Rain days")
        self.rain_days += self.createRows(rain_days_list, "rain days")

    def setSunshine(self, sunshine_list:list):
        self.testLength(sunshine_list, "Sunshine")
        self.sunshine += self.createRows(sunshine_list, "sun")

    def setFooter(self, url:str, title:str):
        footer = '''| source 1 = [[Met Office]]<ref name="MetOffice">{{{{cite web
|url = {}
|title = {}
|publisher = Met Office
|access-date = {}}}}}</ref>
}}}}'''
        
        date_string = date.today().strftime("%B %-d, %Y")
        footer = footer.format(url, title, date_string)
        self.footer = footer

    def getWeatherBox(self) -> str:
        return self.header + self.max_temps + self.min_temps + self.rainfall + self.rain_days + self.sunshine + self.footer

if __name__ == "__main__":
    maxes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    weather_box = weatherBox()
    weather_box.setMaxTemps(maxes)
    print(weather_box.max_temps)