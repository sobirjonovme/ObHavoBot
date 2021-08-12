
import requests

from pprint import pprint
from datetime import date, timedelta

url = "http://api.weatherapi.com/v1/forecast.json?key=9977ea93e56a4044aaf72053211008&"


def pm_to_24(a):
    if "PM" in a:
        a = a.split()[0]
        a = a.split(":")
        a[0] = int(a[0])+12
        return f"{a[0]}:{a[1]}"
    if  "AM" in a:
        a = a.split()[0]
        return a

def kun_qisqa(latitude, longitude, day=''):
    #Berilga kun haqida qisqa ma'lumot
    if day:
        url1 = url + f"q={latitude},{longitude}&dt={day}"
    else:
        url1 = url + f"q={latitude},{longitude}"
    data = requests.get(url1).json()
    shahar = data['location']['name']
    data1 = data['forecast']['forecastday'][0]
    kun = data1['date']
    min_temp = data1['day']['mintemp_c']
    max_temp = data1['day']["maxtemp_c"]
    max_wind = data1['day']['maxwind_kph']
    bosim = int(data['current']["pressure_mb"])
    yomgir = data1["day"]["daily_chance_of_rain"]
    quyosh_chiqishi = pm_to_24(data1['astro']['sunrise'])
    quyosh_botishi =  pm_to_24( data1['astro']['sunset'])
    return shahar, kun, min_temp, max_temp, max_wind, yomgir, quyosh_chiqishi, quyosh_botishi, bosim


def hafta_yasa(latitude, longitude):
    url1 = url + f"q={latitude},{longitude}"
    data = requests.get(url1).json()
    shahar = data['location']['name']
    data1 = data['forecast']['forecastday'][0]
    kun = data1["date"]
    a = kun.split("-")
    day = date(int(a[0]), int(a[1]), int(a[2]))
    lst = []
    for i in range(7):
        b = day + timedelta(i)
        lst.append(str(b))
    return shahar,lst


def kun_batafsil(latitude, longitude, day):
    # Harorat, yogingarchilik, shamol tezligi

    url1 = url + f"q={latitude},{longitude}&dt={day}"
    data = requests.get(url1).json()
    shahar = data['location']['name']
    data1 = data['forecast']['forecastday'][0]["hour"]
    # data1 - list ko'rinshida, har bir element bitta soatlik malumot

    malumot = []
    # bunda <malumot> har bir elementi bir soatlik malumot
    # bir soatlik malumot (soat, harorat, yogin, shamol) ni o'z ichiga oladi

    for a in data1:
        lst = []
        lst.append(a["time"].split()[1])
        lst.append(a["temp_c"])
        lst.append(a["chance_of_rain"])
        lst.append(a["wind_kph"])
        malumot.append(lst)

    return shahar, malumot


if __name__ == "__main__":
    pass
    # print(hafta_yasa(40.41868,71.701709))
    # pprint(kun_batafsil(40.41868, 71.701709, "2021-08-12"))
    # print(pm_to_24("07:18 PM"))
    # funk1(40.41868,71.701709)
        



