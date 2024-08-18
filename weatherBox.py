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
        self.temp_unit:str = "C"
        self.rain_unit:str = "mm"
        self.snow_unit:str = "cm"
        self.header:str = ""
        self.record_highs:str = ""
        self.max_temps:str = ""
        self.mean_temps:str = ""
        self.min_temps:str = ""
        self.record_lows:str = ""
        self.precip:str = ""
        self.precip_days:str = ""
        self.rainfall:str = ""
        self.rain_days:str = ""
        self.snowfall:str = ""
        self.snow_days:str = ""
        self.sunshine:str = ""
        self.humidity:str = ""
        self.dew_point:str = ""
        self.footer:str = ""


    def Americanize(self):
        self.temp_unit = "F"
        self.rain_unit = "in"
        self.snow_unit = "in"


    def setHeader(self, location:str, years: str):
        header = '''{{{{Weather box
| width       = auto
| metric first = yes
| single line = yes
| location    = {} ({})
'''
        self.header = header.format(location, years)
        

    def createRows(self, items: list, row_text: str) -> str:
        rows = ""
        i = 0
        for item in items:
            rows += "| {} {} = {}\n".format(self.months.get(i), row_text, str(item))
            i += 1
        return rows

    
    def list_length_correct(self, input_list: list) -> bool:
        return (len(input_list) == 13 or len(input_list) == 12)
    

    def setRecordHighs(self, record_highs_list:list[float]):
        if self.list_length_correct(record_highs_list):
            self.record_highs = self.createRows(record_highs_list, "record high {}".format(self.temp_unit))

    def setMaxTemps(self, max_temps_list:list[float]):
        if self.list_length_correct(max_temps_list):
            self.max_temps = self.createRows(max_temps_list, "high {}".format(self.temp_unit))

    def setMeanTemps(self, mean_temps_list:list[float]):
        if self.list_length_correct(mean_temps_list):
            self.mean_temps = self.createRows(mean_temps_list, "mean {}".format(self.temp_unit))

    def setMinTemps(self, min_temps_list:list[float]):
        if self.list_length_correct(min_temps_list):
            self.min_temps = self.createRows(min_temps_list, "low {}".format(self.temp_unit))

    def setRecordLows(self, record_lows_list:list[float]):
        if self.list_length_correct(record_lows_list):
            self.record_lows = self.createRows(record_lows_list, "record low {}".format(self.temp_unit))

    def setPrecip(self, precip_list:list[float]):
        if self.list_length_correct(precip_list):
            self.precip = "| precipitation colour = green\n"
            self.precip += self.createRows(precip_list, "precipitation {}".format(self.rain_unit))

    def setPrecipDays(self, precip_days_list:list[float], unit_precip_days:str = "1 mm"):
        if self.list_length_correct(precip_days_list):
            self.precip_days = "| unit precipitation days = {}\n".format(unit_precip_days)
            self.precip_days += self.createRows(precip_days_list, "precipitation days")

    def setRainfall(self, rainfall_list:list[float]):
        if self.list_length_correct(rainfall_list):
            self.rainfall = "| rain colour = green\n"
            self.rainfall += self.createRows(rainfall_list, "rain {}".format(self.rain_unit))

    def setRainDays(self, rain_days_list:list[float], unit_rain_days:str = "1.0 mm"):
        if self.list_length_correct(rain_days_list):
            self.rain_days = "| unit rain days = {}\n".format(unit_rain_days)
            self.rain_days += self.createRows(rain_days_list, "rain days")

    def setSnowfall(self, snow_list:list[float]):
        if self.list_length_correct(snow_list):
            self.snowfall += self.createRows(snow_list, "snow {}".format(self.snow_unit))

    def setSnowDays(self, snow_days_list:list[float], unit_snow_days:str = "1.0 cm"):
        if self.list_length_correct(snow_days_list):
            self.snow_days = "| unit snow days = {}\n".format(unit_snow_days)
            self.snow_days += self.createRows(snow_days_list, "snow days")

    def setHumidity(self, humidity_list:list[float]):
        if self.list_length_correct(humidity_list):
            self.humidity = self.createRows(humidity_list, "humidity")

    def setDewPoint(self, dew_point_list:list[float]):
        if self.list_length_correct(dew_point_list):
            self.dew_point = self.createRows(dew_point_list, "dew point {}".format(self.temp_unit))

    def setSunshine(self, sunshine_list:list[float]):
        if self.list_length_correct(sunshine_list):
            self.sunshine = self.createRows(sunshine_list, "sun")

    def setFooter(self, url:str, title:str, agency:str, format: str|None = None):
        date_string = date.today().strftime("%-d %B %Y")
        footer: str
        if (format == None):
            footer = '''| source 1 = [[{}]]<ref>{{{{cite web
|url = {}
|title = {}
|publisher = {}
|access-date = {}}}}}</ref>
}}}}'''
            footer = footer.format(agency, url, title, agency, date_string)
        else:
            footer = '''| source 1 = [[{}]]<ref>{{{{cite web
|url = {}
|title = {}
|publisher = {}
|format = {}
|access-date = {}}}}}</ref>
}}}}'''
            footer = footer.format(agency, url, title, agency, format, date_string)

        self.footer = footer

    def __str__(self):
        return self.header + self.record_highs + self.max_temps + self.mean_temps + self.min_temps + self.record_lows + self.precip + self.precip_days + self.rainfall + self.rain_days + self.snowfall + self.snow_days + self.humidity + self.dew_point + self.sunshine + self.footer
