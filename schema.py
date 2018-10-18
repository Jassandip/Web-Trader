#!/usr/bin/env python3

import json

from mapper import Database 
#import wrapper
from wrapper import Markit

if __name__ == '__main__':
    # Simple Test
    # print('This is the price of Tesla:',quote(lookup('tesla')))
    with Database('master.db') as db:
        db.create_table('users')
        db.create_table('orders')
        db.create_table('holdings')
        db.add_column('users','username','VARCHAR')
        db.add_column('users','password','VARCHAR')
        db.add_column('users','balance','FLOAT')
        db.add_column('orders','username','VARCHAR')
        db.add_column('orders','ticker_symbol','VARCHAR')
        db.add_column('orders','trade_volume','FLOAT')
        db.add_column('orders','execution_price','FLOAT')
        db.add_column('holdings','username','VARCHAR')
        db.add_column('holdings','ticker_symbol','VARCHAR')
        db.add_column('holdings','trade_volume','FLOAT')
        db.add_column('holdings','vwap','FLOAT')
        print('System agent: Database created.')
