
'''
This program returns the most recent value that was stored persistently
Note: current_eth_price.py must be run before this file since that is where
database.db and eth_table are created
'''

import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# SELECT the most recent stored row in eth_table, and returns stored eth price 
def price_from_db():
    c.execute('''SELECT datetime,value FROM eth_table ORDER BY datetime desc LIMIT 1''')
    user = c.fetchone() 
    print(user[1])

price_from_db()