#!/usr/bin/env python3

from flask import Flask,render_template,request,session,Blueprint

from src.model import model

controller = Blueprint('public',__name__)


@controller.route('/',methods=['GET','POST'])
def loggin():
    if request.method == 'GET':
        message = 'Welcome to web trader, time to make some $$'
        return render_template('loggin.html',message=message)
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        loggin = request.form["loggin"]
        if loggin == "Loggin":
            try:
                session['username'] = model.user_check(password)
                if session['username'] == username:
                    message = session['username'] 
                    return render_template('homepage.html',message=message)
            except:
                message = "Invalid username. Please try another again or sign up"
                return render_template('loggin.html',message=message)
        else:
            model.sign_up(username,password)
            message = 'Signed-up, now logg in with the same credentials'
            return render_template('loggin.html',message=message)

        


@controller.route('/homepage',methods=['GET','POST'])
def hompepage():
    if request.method == 'GET':
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
        for i in users_list:
            if i == session['username']:
                index = users_list.index(i)
                x = users_holdings[index]
                y = volumes[index]
        holdings = []

        for i in range(len(x)):
            amount = prices[x[i]]*y[i][0]
            holdings.append((x[i],y[i][0],amount))
        return render_template('homepage.html',holdings=holdings)
        

@controller.route('/buy',methods=['GET','POST'])
def buy():
    if request.method == 'GET':
        message = 'Make your purchases {}'.format(session['username'])
        return render_template('buy.html',message=message)
    elif request.method == 'POST':
        ticker = request.form["ticker"]
        trade_volume = request.form["quantity"]
        try:
            message = model.buy(session['username'],ticker,trade_volume) 
            return render_template('buy.html',message=message)
        except:
            message = "Something went wrong with the buy function"
            return render_template('buy.html',message=message)

@controller.route('/sell',methods=['GET','POST'])
def sell():
    if request.method == 'GET':
        message = 'What do you wanna sell {}?'.format(session['username'])
        return render_template('sell.html',message=message)
    elif request.method == 'POST':
        ticker = request.form["ticker"]
        trade_volume = request.form["quantity"]
        message = model.sell(session['username'],ticker,trade_volume)
        return render_template('sell.html',message=message)

@controller.route('/lookup',methods=['GET','POST'])
def lookup():
    if request.method == 'GET':
        message = 'What do you wanna to look up {}?'.format(session['username'])
        return render_template('lookup.html',message=message)
    elif request.method == 'POST':
        ticker = request.form["ticker"]
        message = model.lookup(ticker)
        return render_template('lookup.html',message=message)

@controller.route('/quote',methods=['GET','POST'])
def quote():
    if request.method == 'GET':
        message = 'What do you wanna get a quote of {}?'.format(session['username'])
        return render_template('quote.html',message=message)
    elif request.method == 'POST':
        ticker = request.form["ticker"]
        message = model.quote(ticker)
        return render_template('quote.html',message=message)

@controller.route('/leaderboard',methods=['GET','POST'])
def leaderboard():
    if request.method == 'GET':
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
        holdings = []
        while values_final:
            for i in values_final:
                if values_final[i] >= highest:
                    highest = values_final[i]
                    word = i 
            holdings.append((word,highest)) 
            values_final.pop(i)
            highest = 0
        if session['username'][0:5] == 'admin':
            # for i in sorted_words:
            #     print("{} : {}".format(i,sorted_words[i]))

        # for i in range(len(sorted_words)):
        #     holdings.append((sorted_words[i][0],sorted_words[i][1]))
            return render_template('leaderboard.html',holdings1=holdings)
        else: 
            return render_template('haha.html')
        