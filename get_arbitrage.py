
'''
This program returns the name of the currency that has the largest 
price differential percentage between the Gemini and CoinOne exchanges
'''

import requests
import sqlite3
import datetime

# GET eth and btc price from CoinOne API 
url = "https://api.coinone.co.kr/ticker/"

querystr_eth = {"currency":"eth"}
querystr_btc = {"currency":"btc"}

headers_eth = {
    'Cache-Control': "no-cache",
    'Postman-Token': "a3d2e638-3603-4a05-93a6-07dfd52b6c0f"
    }

headers_btc = {
    'Cache-Control': "no-cache",
    'Postman-Token': "c835e6e8-efad-40d6-9a19-c5c5a4cb7ca3"
    }

resp_eth = requests.request("GET", url, headers=headers_eth, params=querystr_eth)
resp_btc = requests.request("GET", url, headers=headers_btc, params=querystr_btc)

j_resp_eth = resp_eth.text
j_resp_eth = resp_eth.json()
j_resp_btc = resp_btc.text
j_resp_btc = resp_btc.json()

# GET eth and btc price from Gemini API 
url1 = "https://api.gemini.com/v1/pubticker/ethusd"
url2 = "https://api.gemini.com/v1/pubticker/btcusd"

headers1 = {
    'Cache-Control': "no-cache",
    'Postman-Token': "8c32cd47-046c-4efc-bd22-6107280b3c95"
    }

headers2 = {
    'Cache-Control': "no-cache",
    'Postman-Token': "499fce59-07b7-4266-a9f7-3106908d3ac8"
    }

response1 = requests.request("GET", url1, headers=headers1)
response2 = requests.request("GET", url2, headers=headers2)

j_response1 = response1.text
j_response1 = response1.json()
j_response2 = response2.text
j_response2 = response2.json()

# Persistent Storage 
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Creates Gemini table and Coinone table with categories: datetime, eth price, btc price 
def make_table():
    c.execute('CREATE TABLE IF NOT EXISTS gemini_table (datetime INT, eth INT, btc INT)')
    c.execute('CREATE TABLE IF NOT EXISTS coinone_table (datetime INT, eth INT, btc INT)')

# inputs result from GET into gemini_table 
def input_entry_g(datetime, eth, btc):
    c.execute("INSERT INTO gemini_table (datetime, eth, btc) VALUES (?,?,?)",
              (datetime,eth,btc))
    conn.commit()

# inputs result from GET into eth_table
def input_entry_c(datetime, eth, btc):
    c.execute("INSERT INTO coinone_table (datetime, eth, btc) VALUES (?,?,?)",
              (datetime,eth,btc))
    conn.commit()
    
# SELECT the most recent stored row in gemini_table; returns [eth price, btc price]
def price_from_g_db():
    c.execute('''SELECT datetime,eth FROM gemini_table ORDER BY datetime desc LIMIT 1''')
    eth = c.fetchone() 
    c.execute('''SELECT datetime,btc FROM gemini_table ORDER BY datetime desc LIMIT 1''')
    btc = c.fetchone()
    return [eth[1],btc[1]]
    
# SELECT the most recent stored row in eth_table; returns [eth price, btc price]
def price_from_c_db():
    c.execute('''SELECT datetime,eth FROM coinone_table ORDER BY datetime desc LIMIT 1''')
    eth = c.fetchone() 
    c.execute('''SELECT datetime,btc FROM coinone_table ORDER BY datetime desc LIMIT 1''')
    btc = c.fetchone()
    return [eth[1],btc[1]]

# returns differential percentage between v1, v2
def diff_percentage(v1,v2):
    return 100* (abs(v1-v2)/((v1+v2)/2))
    
#MAIN---------------------------------------------
make_table()

datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4])
input_entry_g(datetime, j_response1['last'], j_response2['last'])
# params: convert Korean Won -> USD 
input_entry_c(datetime, int(j_resp_eth['last'])/1000, int(j_resp_btc['last'])/1000)

gemini_price_li = price_from_g_db()
coinone_price_li = price_from_c_db()

eth_dif = diff_percentage(gemini_price_li[0],coinone_price_li[0])
btc_dif = diff_percentage(gemini_price_li[1],coinone_price_li[1])

if (eth_dif > btc_dif):
    print("ethereum")
else:
    print("bitcoin")

c.close()
conn.close()