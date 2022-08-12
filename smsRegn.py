import urllib.request
import urllib.parse
import json
import pickle
import requests
import urllib
import mysql
import datetime
import time

def getMessages(apikey, inboxID):
    params = {'apikey': 'ZpPu6fA9IgY-AuxN59AFKYRJdHFrEL9c99xDzpLBIe', 'inbox_id': inboxID}
    f = urllib.request.urlopen('https://api.textlocal.in/get_messages/?'
                               + urllib.parse.urlencode(params))
    return (f.read(), f.code)

def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

# db = mysql.connector.connect(host='localhost', user='D_S', passwd='sih19', database = 'SiH') #Here import the file which has set of different pincodes of farmers regd in our system.
# cursor = db.cursor()

pickle_j = load('pickle_i.pickle')
#print(pickle_j)
resp, code = getMessages('ZpPu6fA9IgY-AuxN59AFKYRJdHFrEL9c99xDzpLBIe', '10')
#print(resp)
x = resp.decode()
#print(x)
#print(x)
j = json.loads(x)
#print(j)
dic = dict()
url = 'http://13.126.31.37:8000/sms-signup'
#print(j['num_messages'])
for i in range(pickle_j, j['num_messages']):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    temp = j['messages'][i]['message']
    #print(temp)
    #print(type(temp))
    l_temp = temp.split()
    l_temp[4] = l_temp[4].lower()
    #try:
    dic['name'] = l_temp[1]
    print(type(l_temp[1]))
    dic['phone'] = l_temp[2]
    dic['pincode'] = l_temp[3]
    dic['lang'] = l_temp[4]
    js = json.dumps(dic)

    #print(dic)
    pickle_j += 1
    # sql = "INSERT INTO base (name, phn_no, pinCode, timestamp, language) VALUES (%s, %s %s %s %s)"
    # val = (l_temp[1], l_temp[2], l_temp[3], st, l_temp[4])
    #cursor.execute(sql, val)
    #db.commit()
    #request = urllib.request.Request(url, encoded_dict)
    requests.post(url, json=dic, headers={'Content-Type': 'application/json'})
    #js = json.dumps(dic)
    #print(type(dic))
        #r = requests.post(url='http://13.126.31.37:8000/signup', data=)
#        print(dic) #Send to server
    #sending a JSON of : 'name'    'ph_no'    'pincode'    'lang'

    #except:
     #   print('-1')

with open('pickle_i.pickle', 'wb') as fobj:
    pickle.dump(pickle_j, fobj)
#js = json.dumps(dic)
#print(js)
#print(dic)
#print(pickle_j)
