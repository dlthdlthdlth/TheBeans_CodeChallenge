
'''
 This program returns the current price of ethereum in Korean Won and 
 stores the result of such query to sqlite database
'''

import requests
import json
import sqlite3
import datetime

# GET request to CoinOne's public API to get current price of ethereum
url = "https://api.coinone.co.kr/ticker/"

querystring = {"currency":"eth"}

headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "a3d2e638-3603-4a05-93a6-07dfd52b6c0f"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
j_response = response.text
j_response = json.loads(j_response)

# Store the result of above query into database.db 
conn = sqlite3.connect("database.db")
c = conn.cursor()

# makes table in database with categories: datetime, currency, value (price)
def make_table():
    c.execute('CREATE TABLE IF NOT EXISTS eth_table (datetime INT, currency TEXT, value INT)')

# inputs result from GET into table
def input_entry(datetime, currency, value):
    c.execute("INSERT INTO eth_table (datetime, currency, value) VALUES (?,?,?)",
              (datetime,currency,value))
    conn.commit()

#MAIN---------------------------------------------
datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
currency = "ethereum"
value = j_response['last']

# prints current price of ethereum in Korean Won
print(value)

make_table()
input_entry(datetime, currency, value)

c.close()
conn.close()