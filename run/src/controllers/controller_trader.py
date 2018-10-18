#!/usr/bin/env python3

import model
import view

from operator import itemgetter

# Note: we could write the following as well:
#while True:
def game_loop():
    start = view.start_up_menu()
    if start == "s":
        (user_name,password) = view.sign_up_menu()
        model.sign_up(user_name,password)
    else:
        (user_name,password) = view.logg_in_menu()
        _id = model.user_check(password) 
        print(_id)
    
    while 1:
        buy_inputs = ['b','buy']
        sell_inputs = ['s','sell']
        lookup_inputs = ['l','lookup','look up','look-up']
        quote_inputs = ['q','quote']
        exit_inputs = ['e','exit','quit']
        view_inputs = ['v']
        leader_board_inputs = ['l']
        acceptable_inputs = buy_inputs     \
                            +sell_inputs   \
                            +lookup_inputs \
                            +quote_inputs  \
                            +exit_inputs   \
                            +view_inputs   \
                            +leader_board_inputs
        user_input = view.main_menu()
        if user_input in acceptable_inputs:
            if user_input in buy_inputs:
                balance = model.check_balance(user_name)
                fee = 6.25
                ticker_symbol = view.quote_menu()
                price = model.quote(ticker_symbol)
                trade_volume = view.transaction_menu(balance,ticker_symbol,price)
                transaction_cost = (float(trade_volume)*price)+fee 
                if transaction_cost <= balance:
                    balance -= transaction_cost
                    model.update_cash(user_name,balance)
                    model.buy(user_name,ticker_symbol,float(trade_volume),float(price))
                    model.buy_holdings(user_name,ticker_symbol,float(trade_volume),price)
                else:
                    print("Not enough monay")
                
            elif user_input in sell_inputs:
                ticker_symbol = view.quote_menu()
                price = model.quote(ticker_symbol)
                trade_volume = view.sell_menu()
                owned = model.check_holdings(user_name,ticker_symbol)
                if owned and int(trade_volume) <= owned:
                    model.sell_holdings(user_name,ticker_symbol,trade_volume,price,owned)
                else:
                    print("You dont have that to sell")
            elif user_input in lookup_inputs:
                return model.lookup(view.lookup_menu())
            elif user_input in quote_inputs:
                return model.quote(view.quote_menu())
            elif user_input in exit_inputs:
                break
            elif user_input in leader_board_inputs or view_inputs:
                users = model.get_users()
                users_list = [] # this is a list of all the users that currenttly have holdings
                for i in users:
                    users_list.append(i[0]) 
                
                users_holdings = [] # users holdings by tickers but not numbers 
                for i in users_list:
                    user_holdings = model.get_holdings(i)
                    a = []
                    for i in user_holdings:
                        a.append(i[0])
                    users_holdings.append(a)

                tickers = [] # is all the stocks the users, un "set'd" and joinined together
                for i in users_holdings:    
                    for j in i:
                        tickers.append(j)
                prices = {}  # this has all the prices for all the stocks owned in the holdings
                for i in set(tickers): #
                    price = model.quote(i)
                    prices[i]= price

                volumes = []   # a list of lists of amount of stock each of them own
                for i in users_list:
                    volumes.append(model.holdings_volumes(i))
                
                values_final = {}
                for i in range(len(users_holdings)):
                    total = 0
                    for j in range(len(users_holdings[i])):
                        total+=(prices[users_holdings[i][j]])*(volumes[i][j][0])
                    values_final[users_list[i]]=total  
                highest = 0 
                sorted_words = {}
                while values_final:
                    for i in values_final:
                        if values_final[i] >= highest:
                            highest = values_final[i]
                            word = i 
                    sorted_words[word] = highest 
                    values_final.pop(i)
                    highest = 0
                if user_name[0:5] == 'admin':
                    view.leader_board()
                    for i in sorted_words:
                        print("{} : {}".format(i,sorted_words[i]))
                
                balance = model.check_balance(user_name)
                view.show_balance(balance)
                for i in users_list:
                    if i == user_name:
                        index = users_list.index(i)
                        x = users_holdings[index]
                        y = volumes[index]
                for i in range(len(x)):
                    amount = prices[x[i]]*y[i][0]
                    print('{} : {}'.format(x[i],amount))
            


if __name__ == '__main__':
    print(game_loop())

    
