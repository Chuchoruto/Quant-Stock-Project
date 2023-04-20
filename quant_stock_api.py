from flask import Flask, request, send_file
import redis
import requests
import json
import os
import matplotlib.pyplot as plt
import io
import yfinance as yf

app = Flask(__name__)

def get_redis_client():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)

def get_redis_image_db():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=1)

def get_ticker_db():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=2, decode_responses=True)

rd = get_redis_client()

rd_image = get_redis_image_db()

rd_tickers = get_ticker_db()

@app.route('/tickers/<ticker>', methods = ['POST'])
def post_tickers(ticker: str) -> str:
    '''
    Gets or Deletes the desired tickers stored in the redis db

    Args: None

    Returns: String stating success or failure
    '''
    if(len(rd_tickers.keys())==0):
        tickers = []
    else:
        tickers = rd_tickers.get("Tickers")
    tickers.append(yf.download(ticker))
    rd_tickers.set("Tickers", tickers)

    return "Tickers posted"
        


@app.route('/tickers', methods = ['GET', 'DELETE'])
def handle_tickers():
    '''
    Gets or Deletes the desired tickers stored in the redis db

    Args: None

    Returns: Something corresponding to which method was used
        "DELETE" method: deletes all tickers in redis db
        "GET" method: returns list of all tickers listed in redis db
    '''


@app.route('/data', methods = ['GET', 'POST', 'DELETE'])
def handle_data() -> list:
    '''
    Manipulates data wiht 3 different methods with GET, POST, and DELETE method

    Args: None

    Returns: String corresponding to which method was used
        "DELETE" method: deletes all data in redis db
        "POST" method: posts data into redis db
        "GET" method: returns data from redis db
    '''

    method = request.method
    global rd

    if method == 'POST':
         return "Data posted"
    
    elif method == 'GET':
        return "Here is your data"
        

    elif method == 'DELETE':
        rd.flushdb()
        return f'data deleted, there are {len(rd.keys())} keys in the db\n'

    else:
        return 'the method you tried is not supported\n'

    return f'method completed \n'


@app.route('/plot/<imageID>?<stock1>&<stock2>', methods = ['GET', 'POST', 'DELETE'])
def handle_data() -> list:
    '''
    Plot stocks, given by queiry parameters <stock1> and <stock2>


    '''


    return 0



@app.route('/compare', methods = ['GET', 'POST', 'DELETE'])
def handle_data() -> list:
    '''
    Compare 2 stocks

    - Quiry Parameters?
    '''

    return 0



@app.route('/data', methods = ['GET', 'POST', 'DELETE'])
def handle_data() -> list:
    '''
    Some function
    '''

    return 0




if __name__ == '__main__':
    # can put debug config here
    app.run(debug=True, host='0.0.0.0')
