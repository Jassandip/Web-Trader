#!/usr/bin/env python3

import json

from src.mapper.mapper import Database 
from src.wrapper.wrapper import Markit

import requests

def buy(user_id,ticker_symbol,trade_volume):
        price = quote(ticker_symbol)  
        balance = check_balance(user_id)
        fee = 6.25
        transaction_cost = (float(trade_volume)*price)+fee
        if transaction_cost <= balance:
                buy_execute(user_id,ticker_symbol,trade_volume,price)
                balance -= transaction_cost
                update_cash(user_id,balance)
                buy_holdings(user_id,ticker_symbol,trade_volume,price)
                return "Congratulations you have purchased {} stocks of {}".format(trade_volume,ticker_symbol)
        else:
                return "Not enough money"


def buy_execute(user_id,ticker_symbol,trade_volume,price):
        with Database('master.db') as db:
                db.insert_4('orders','username','ticker_symbol','trade_volume','execution_price',user_id,ticker_symbol,float(trade_volume),float(price))

def sell(user_name,ticker_symbol,trade_volume):
        price = quote(ticker_symbol)  
        balance = check_balance(user_name)
        owned = float(check_holdings(user_name,ticker_symbol))
        if owned >= float(trade_volume):
                with Database('master.db') as db:
                        new_owned = owned - float(trade_volume) 
                        db.update_holding(user_name,ticker_symbol,new_owned)
                        new_balance = balance + (float(trade_volume)*float(price)) - 6.25
                        db.update_cash(user_name,new_balance)
                        db.insert_4('orders','username','ticker_symbol','trade_volume','execution_price',user_name,ticker_symbol,trade_volume,price)
                return "Congratulations toy just sold {} stocks of {}".format(trade_volume,ticker_symbol)
        else:
                return "You don't have that many to sell"

           
def sell_execute():
    pass

def lookup(company_name):
    #endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input='+company_name
    #response = json.loads(requests.get(endpoint).text)
    #return response[0]['Symbol']
    with Markit() as m:
        return m.lookup(company_name)

def quote(ticker_symbol):
    with Markit() as m:
        return m.quote(ticker_symbol)


def sign_up(username,password):
    with Database('master.db') as db:
        db.sign_up(username,password)

def user_check(password):
    with Database('master.db') as db:
        username = db.user_check(password)
        return username

def check_balance(user_id):
    with Database('master.db') as db:
        return db.check_balance(user_id)

def buy_holdings(user_name,ticker_symbol,trade_volume,price):
    with Database('master.db') as db:
        try:
                current = db.check_holdings(user_name,ticker_symbol)
                new_current = float(trade_volume) + current 
                db.update_holding(user_name,ticker_symbol,new_current)
        except:
                db.new_holding(user_name,ticker_symbol,trade_volume,(price*float(trade_volume)))



def update_cash(username,balance):
    with Database('master.db') as db:
        return db.update_cash(username,balance)

def check_holdings(user_name,ticker_symbol):
    with Database('master.db') as db:
        try:
            return db.check_holdings(user_name,ticker_symbol)
        except:
            return False 

def get_users():
    with Database('master.db') as db:
        return db.get_users()

def get_holdings(user_name):
    with Database('master.db') as db:
        return db.get_holdings(user_name)

def holdings_volumes(user_name):
    with Database('master.db') as db:
        return db.holdings_volumes(user_name)




        












