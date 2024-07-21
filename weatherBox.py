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
    LIST_LENGTH: int = 13

    def __init__(self):
        self.header:str = ""
        self.max_temps:str = ""
        self.min_temps:str = ""
        self.rainfall:str = ""
        self.rain_days:str = ""
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
        
    def createRows(self, items: list, row_text: str):
        rows = ""
        i = 0
        for item in items:
            rows += " | {} {} = {}\n".format(self.months.get(i), row_text, item)
            i += 1
        return rows
    
    def list_length_correct(self, input_list: list) -> bool:
        return len(input_list) == self.LIST_LENGTH

    def setMaxTemps(self, max_temps_list:list):
        if self.list_length_correct(max_temps_list):
            self.max_temps = self.createRows(max_temps_list, "high C")

    def setMinTemps(self, min_temps_list:list):
        if self.list_length_correct(min_temps_list):
            self.min_temps = self.createRows(min_temps_list, "low C")

    def setRainfall(self, rainfall_list:list):
        if self.list_length_correct(rainfall_list):
            self.rainfall = " | rain colour = green\n"
            self.rainfall += self.createRows(rainfall_list, "rain mm")

    def setRainDays(self, rain_days_list:list):
        if self.list_length_correct(rain_days_list):
            self.rain_days = " | unit rain days = 1 mm\n"
            self.rain_days += self.createRows(rain_days_list, "rain days")

    def setSunshine(self, sunshine_list:list):
        if self.list_length_correct(sunshine_list):
            self.sunshine = self.createRows(sunshine_list, "sun")

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
