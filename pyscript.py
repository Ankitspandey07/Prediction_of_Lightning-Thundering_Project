import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
import requests
import mysql.connector
import datetime
import pickle
import json
import csv
import testcall

def getDate():
    date = str(datetime.date.today())
    date = date[5:]
    l = date.split('-')
    #print(l)
    l[0], l[1] = l[1], l[0]
    date = ''
    date += date.join(l)
    return date

date = getDate()
date = date[:2] + '-' + date[2:]
db = mysql.connector.connect(host='localhost', user='D_S', passwd='sih19', database = 'SiH') #Here import the file which has set of different pincodes of farmers regd in our system.
cursor = db.cursor()
cursor.execute('SELECT * from timeTab')
all_pin_time = cursor.fetchall()
cursor = db.cursor()
# file = open('City_data_all.csv') # Remove the code and make dictionary here
# files = csv.reader(file)  # Remove the code and make dictionary here
#
# file = open('IN_final_running.csv') # Remove the code and make dictionary here
# files = list(csv.reader(file))
# order = {}
# order['cloudy'] = 0.50
# order['partly'] = 0.50
# order['rain'] = 0.85
# order['thunderstorm'] = 0.90
# order['thundershowers'] = 0.90
# order['spells'] = 0.65
# order['haze'] = 0.4
# order['lightning'] = 0.95
# order['thunder'] = 0.85
# order['thundery'] = 0.85
order = {}
order['cloudy'] = 0.74
order['partly'] = 0.74
order['rain'] = 0.83
order['thunderstorm'] = 0.95
order['thundershowers'] = 0.90
order['spells'] = 0.65
order['haze'] = 0.4
order['lightning'] = 1.0
order['thunder'] = 0.85
order['thundery'] = 0.85

lightning_words = ['cloudy', 'partly cloudy', 'rain', 'thunderstorm', 'thundershowers', 'spells', 'haze', 'lightning', 'light', 'thunder', 'thundery']
with open('hash_table.pickle', 'rb') as handle:
    hash_table = pickle.load(handle)
def getCity(pin):
    try:
        return str(hash_table[str(pin)][2])
    except:
        return -1
    #Create a dictionary of Kirath's Pin code file. Use it here as key value pair.!



def getCityId(pin):
    #Use Kirath's CSV as dictionary here
    try:
        return hash_table[str(pin)][1]
    except:
        return -1


def getAQI(pin):
    city = getCity(pin)
    print(city)
    if city == -1:
        return -1
    key ='579b464db66ec23bdd000001ebe4b78eeb0b42bb4b739cf055d7a0b4'
    link = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key="+key+"&format=json&filters[city]="+city+"&filters[pollutant_id]=PM10&filters[pollutant_id]=PM2.5"
    try:
        response = requests.get(link)
        data = response.json()
        count = 1
        s = 0
        for station in data['records']:
            if station['pollutant_avg'] != 'NA':
                s = s + int(station['pollutant_avg'])
                count += 1
        avg = s // count
        return avg
    except:
        return -1


def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, 'html5lib')
    return soupdata


def getForecast(pin):
    city_code = getCityId(pin)
    if city_code == -1 or city_code == 0:
        return -1
    y = city_code
    x = "http://city.imd.gov.in/citywx/city_weather.php?id=" + y
    soup = make_soup(x)
    tables = soup.body.center.table.find_all('table')
    rows = soup.find_all('tr')
    lower_table = tables[1].find_all('tr')
    rows = lower_table[2:]
    arr = []
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            cell_content = cell.getText()
            clean_content = re.sub('\t+', ' ', cell_content).strip()
            arr.append(clean_content)
    data = []
    temp = []
    for i in arr:
        if i != '':
            temp.append(i)
    for i in range(len(temp)):
        if (i + 1) % 4 == 0:
            data.append(temp[i])
            break
        else:
            data.append(temp[i])
    return data
    # df = pd.DataFrame(data)
    # df.columns = ['Date', 'MinTemp', 'MaxTemp', 'Forecast']
    # df.to_json('out2.json')


#file = open('City_data.csv') #Here import the file which has set of different pincodes of farmers regd in our system.
#files = csv.reader(file)
# for row in files:
#    probability = 0
#    print('Trying {}'.format(row[1]))
#    temp = getForecast(row[1])
#    forecast = temp[3]
#    forecast = forecast.lower()
#    forecast_word = word_tokenize(forecast)
#    for word in forecast_word:
#        if word in lightning_words:
#            if order[word] > probability:
#                probability = order[word]
#    print(probability)
def normalise(number):
    return (number) / 500 

def lightningProbability(pin):
    # for row in files:  #Traverse through different pincodes of farmers in our system
    try:
        probability = 0
        # print('Trying {}'.format(row[8]))
        temp = getForecast(pin)
        forecast = temp[3]
        forecast = forecast.lower()
        forecast_word = word_tokenize(forecast)
        for word in forecast_word:
            if word in lightning_words:
                if order[word] > probability:
                    probability = order[word]
        return probability
    except:
        return -1
# def callme():
#     cursor.execute('SELECT * from timeTab')
#     get_all = cursor.fetchall()
#     pincodes = []
#     for each in get_all:
#         time = each[1]
#         if time == date:
#             pincodes.append(each[0])
#     for i in range(len(pincodes)):
#         sql = 'SELECT * from a'+ pincodes[i]
#         cursor.execute(sql)
#         all_detail = cursor.fetchall()
#         for obj in all_detail:
#             ph = obj[1]
#             testcall.connect_customer(sid='student580', token = 'edc82e540212f12b53c661755600bbc2d79d5a96',exotel_no=ph,callerid="08047103685", url = 'http://13.127.181.8:8000/get-audio-demo', timelimit=None, timeout=None,calltype="trans",
#                      callback_url=None)


def controller():
    final_probability = 0
    arr = []
    for each in all_pin_time:
        lp = lightningProbability(each[0])
        aqi = getAQI(each[0])
        print("-"*40)
        print("LP : {}".format(lp))
        print("AQI : {}".format(aqi))
        if lp != -1 and aqi != -1:
            norm_aqi = normalise(aqi)
            final_probability = 0.1 * norm_aqi + 0.9 * lp

        elif lp != -1 and aqi == -1:
            final_probability = lp
        print("Final Probability : {}".format(final_probability))
        print("="*40)
        if final_probability >= 0.75:
            #temp_sql = "UPDATE timeTab SET date = " + date + " where pinCode = " + (each[0])
            arr.append(each[0])
            sql = "UPDATE timeTab SET date = " +"'" + date + "'"+" where pinCode = " + "'" + (each[0]) +"'"
            # sql = temp_sql[:-7] + "'" + temp_sql[-6:] + "'"
            # sql = sql[:26] + "'" + sql[26:31] + "'" + sql[31:]
            cursor.execute(sql)
            db.commit()

    return arr, date


def main():
    arr, date = controller()
    print(arr, date)
    #lj = json(arr)
    url = 'http://13.126.31.37:8000/azib'
    # data = {'0' : date, '1' : lj}
    payload = {"date": date}
    requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    # a = requests.post(link, data, headers={'content-type': 'application/json'})


if __name__ == '__main__':
    main()








