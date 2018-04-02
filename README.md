# Coding Challenge: The Beans 

### Prerequisites

* download Python3: https://www.python.org/downloads/ 
* download this repo 
* use any IDE that supports Python to run files  

### Tools Used 

* Postman API Development Enviroment 
* DB Browser for SQLite 
* Spyder IDE

### Funtionality of Each File
Execution order should be in this order. 
* `current_eth_price.py` : returns the current price of ethereum in Korean Won and stores the result of such query to sqlite database. 
* `get_last_eth_price.py`: returns the most recent value that was stored persistently
* `get_arbitrage.py`: returns the name of the currency that has the largest price differential percentage between the Gemini and CoinOne exchanges 

## API

* [CoinOne](http://doc.coinone.co.kr) 
* [Gemini](https://docs.gemini.com/rest-api/) 

## Acknowledgments

* Python sqlite3 documentation 
* YouTuber sentdex's videos on sqlite3 
* Lots of StackOverflow articles & Google searches
