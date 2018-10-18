#!/usr/bin/env pyhton3

import sqlite3 

class Database: 
    def __init__(self,database_name):
        self.connection = sqlite3.connect(database_name,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
    
    def create_table(self,_tablename):
        self.cursor.execute(
            """CREATE TABLE {}(
                pk INTEGER PRIMARY KEY AUTOINCREMENT
            );""".format(
                _tablename
            ) 
        )
    
    def add_column(self,_tablename,_columnname,_columntype):
        self.cursor.execute(
            """ALTER TABLE {} ADD COLUMN {} {};""".format(_tablename,_columnname,_columntype))
    
    def insert_3(self,_tablename,_column1,_column2,_column3,_value1,_value2,_value3):
        self.cursor.execute(
            """INSERT INTO {}({},{},{}) VALUES (
                {},{},{}
            );""".format(_tablename,_column1,_column2,_column3,_value1,_value2,_value3))

    def insert_4(self,_tablename,_column1,_column2,_column3,_column4,_value1,_value2,_value3,_value4):
        self.cursor.execute(
            """INSERT INTO {}({},{},{},{})VALUES (
                '{}','{}',{},{}
            )

            ;""".format(_tablename,_column1,_column2,_column3,_column4,_value1,_value2,_value3,_value4))

    def sign_up(self,_username,_password):
        self.cursor.execute(
            """INSERT INTO users(
                username,
                password,
                balance
            ) VALUES(
                '{username}',
                '{password}',
                {balance}
            );""".format(
                username=_username,
                password=_password,
                balance=10000.
            )
        )


    def user_check(self,password):
        self.cursor.execute("""SELECT username FROM users WHERE password == '{}';""".format(password))
        user = self.cursor.fetchone()[0]
        return user 

    def check_balance(self,user_name):
        self.cursor.execute("""SELECT balance FROM users WHERE username=='{}';""".format(user_name))
        return self.cursor.fetchone()[0]

    def check_holdings(self,user_name,ticker_symbol):
        self.cursor.execute("""SELECT trade_volume FROM holdings WHERE username=='{}' AND ticker_symbol=='{}' 
        ;""".format(user_name,ticker_symbol))
        return self.cursor.fetchone()[0]

    def new_holding(self,_value1,_value2,_value3,_value4):
        self.cursor.execute(
            """INSERT INTO holdings(username, ticker_symbol, trade_volume, vwap) VALUES (
                '{}','{}',{},{}
            );""".format(_value1,_value2,_value3,_value4))

    def update_holding(self,username,ticker_symbol,new_trade_volume):
        self.cursor.execute("""UPDATE holdings SET trade_volume = {} 
        WHERE username = '{}' 
        AND ticker_symbol = '{}'
        ;""".format(new_trade_volume,username,ticker_symbol))

    def update_cash(self,username,balance):
        self.cursor.execute("""UPDATE users SET balance = {} 
        WHERE username=='{}'
        ;""".format(balance,username))

    def get_users(self):
        self.cursor.execute("""SELECT username FROM users;""")
        return self.cursor.fetchall()

    def get_holdings(self,username):
        self.cursor.execute("""SELECT ticker_symbol FROM holdings WHERE username=='{}';""".format(username))
        return self.cursor.fetchall()

    def holdings_volumes(self,user_name):
        self.cursor.execute("""SELECT trade_volume FROM holdings WHERE username=='{}';""".format(user_name))
        return self.cursor.fetchall()