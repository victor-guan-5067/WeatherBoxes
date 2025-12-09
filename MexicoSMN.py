import requests
from weatherBox import weatherBox


def makeWeatherBox(location, normals_page, normals_url, extremes_page, extremes_url) -> str:

    normals_lines = normals_page.split('\n')

    weather_box = weatherBox()
    weather_box.setHeader(location, "1991–2020 normals, extremes")

    func = None
        
    for line in normals_lines:

        if (line.startswith("TEMPERATURA MÁXIMA")):
            func = weather_box.setMaxTemps
        if (line.startswith("TEMPERATURA MÍNIMA")):
            func = weather_box.setMinTemps
        if (line.startswith("TEMPERATURA MEDIA")):
            func = weather_box.setMeanTemps
        if (line.startswith("PRECIPITACIÓN")):
            func = weather_box.setPrecip
        if (line.startswith("EVAPORACIÓN")):
            func = None
        if (line.startswith("NÚMERO DE DÍAS CON LLUVIA")):
            func = weather_box.setPrecipDays

        if (len(line) >= 6 and line.split()[0] == 'NORMAL' and func !=None):
            data = line.split()[1:]
            for i in range(len(data)):
                if '.' not in data[i]:
                    data[i] = data[i] + '.0'
            func(data)

    
    extremes_lines = extremes_page.split('\n')

    highs_list = []
    lows_list = []

    i = 0
    func = None

    for line in extremes_lines:
        if (line.startswith("TEMPERATURA MÁXIMA")):
            func = weather_box.setRecordHighs
            highs_list = []
            i = 0
        if (line.startswith("TEMPERATURA MÍNIMA")):
            func(highs_list)
            func = weather_box.setRecordLows
            highs_list = []
            i = 0

        if (func == weather_box.setRecordHighs and 3 <= i <= 14):
            data = line.split()[4]
            highs_list.append(data)

        if (func == weather_box.setRecordLows and 3 <= i <= 14):
            data = line.split()[7]
            lows_list.append(data)

        i += 1

    func(lows_list)

    weather_box.setFooter("Servicio Meteorológico Nacional (Mexico)|Servicio Meteorológico Nacional", normals_url, 'NORMAL CLIMATOLÓGICA 1991-2020', agency="Servicio Meteorológico Nacional", format="TXT")
    weather_box.setFooter2(extremes_url, 'VALORES EXTREMOS', agency="Servicio Meteorológico Nacional", format="TXT")

    return str(weather_box)


if __name__ == "__main__":
    location:str = input("location: ")

    normals_url:str = input("Climate averages (1991-2020) webpage: ")
    normals_page = requests.get(normals_url).text

    extremes_url:str = input("Climate extremes webpage: ")
    extremes_page = requests.get(extremes_url).text

    weather_box:str = makeWeatherBox(location, normals_page, normals_url, extremes_page, extremes_url)
    with open("weatherbox.txt", "w") as file:
        file.write(weather_box)
    