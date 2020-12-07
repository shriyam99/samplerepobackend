import yfinance as yf
import numpy as np
import sys
import asyncio
import pandas as pd
# import glob
import requests
import os
import json
import csv

from GoogleNews import GoogleNews
from newspaper import Article

import pickle

import tensorflow as tf
# import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard

#%matplotlib inline

from sklearn.preprocessing import StandardScaler

# Import Libraries and packages from Keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam


#sort_orders=[]

#duration=int(0)
#amount=int(0)

def para(duration, amount):
    f = open('companies.json',)
    s = open('companies1.json',)
    x = "http://localhost:8081/getCompanyData"
    y = "http://localhost:8081/getAnalysis"

    data = json.load(f)
    data1 = json.load(s)
    cmp = []
    value = []
    df = {}
    for i in data['allCompanies']:
        cal = []
        url = x+i
        response = requests.get(url)
        d = response.text
        parsed = json.loads(d)
        ans = 0
        cmpName = parsed['name']
        price = parsed['price']
        tmp = yf.Ticker(cmpName+".NS")
        y = tmp.info
        eps = y["trailingEps"]
        if(float(price) <= float(amount)):
            for l in parsed['data']:
                t = l["period"]
                lvl = l["level"]
                ind = l["indication"]
                if(t == "MACD(12,26,9)"):
                    if(lvl > '0'):
                        cal.append("Bullish")
                    else:
                        cal.append("Bearish")

                if(t == "RSI(14)"):
                    if(lvl > '70'):
                        cal.append("Bearish")
                    elif(lvl < '30'):
                        cal.append("Bullish")
                    else:
                        cal.append("Neutral")


                if(t == "Stochastic(20,3)"):
                    if(lvl > '80'):
                        cal.append("Bearish")
                    else:
                        cal.append("Bullish")

                if(t == "ROC(20)"):
                     if(lvl > '0'):
                        cal.append("Bullish")
                     else:
                        cal.append("Bearish")


                if(t == "CCI(20)"):
                    if(lvl > '100'):
                        cal.append("Bearish")
                    elif(lvl > '100'):
                        cal.append("Bullish")
                    else:
                        cal.append("Bearish")


                if(t == "RSC (6 months)"):
                    if(ind =="Outperformer"):
                        cal.append("Bullish")
                    else:
                        cal.append("Bearish")


                if(t == "ADX(14)"):
                    if(lvl > "25"):
                        cal.append("Bullish")
                    else:
                        cal.append("Bearish")
                        
            ans = 0
            
            if(duration > 30):
                if(eps < 0):
                    cal.append("Bearish")
                else:
                    cal.append("Bullsih")
  

        for i in cal:
            if(i == "Bullish"):
                ans+=1
        cmpName = cmpName + ".NS"
        df[cmpName] = ans

    sort_orders = sorted(df.items(), key=lambda x: x[1], reverse=True)

    #for i in sort_orders:
    #	print(i[0], i[1])


    f.close()
    s.close()



    tickers = []

    for t in sort_orders[:6]:
        tickers.append((t[0].split('.'))[0].lower())


    headline=[]

    gtickers= tickers[:3]

    for tick in gtickers:
        googlenews=GoogleNews(start='11/01/2020',end='11/25/2020')
        googlenews.search(tick)

        for i in range(2,4):
            googlenews.getpage(i)
            result=googlenews.result(sort=False)
            df=pd.DataFrame(result)
            #df.reset_index(inplace=True)
            df.replace("[^a-zA-Z]"," ",regex=True, inplace=True)
            df['title'] = df['title'].str.lower()
            headline.append(' '.join(str(x) for x in df['title']))
            #print(df['title'])
            #df = df.loc[0:24]
            print(df)



    with open('stock_senti_analysis_final_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('stock_senti_analysis_final_model.pkl', 'rb') as fr:
        model = pickle.load(fr)


    test_df = vectorizer.transform(headline)
    additional_mk = model.predict(test_df)

    print("news headline out")
    print(additional_mk)


    ytickers = []

    for i in range(0,4): #sort_orders[:6]:
        if(additional_mk[i]):
            ytickers.append((sort_orders[i])[0])

    for i in range(4,7):
        ytickers.append((sort_orders[i])[0])

    newls = []
    with open('alltickers.txt', 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            current_place = line[:-1]
            newls.append(current_place)

    commonls = list((set(ytickers)).intersection(set(newls)))

    print(commonls)
    with open('allTickers.txt', 'a') as fp:
        for y in ytickers:
            if y not in commonls:
                fp.write(y+"\n")

    # ---> Special function: convert <datetime.date> to <Timestamp>
    def datetime_to_timestamp(x):
        '''
            x : a given datetime value (datetime.date)
        '''
        return datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')


    DF_pred=[]
    for tick in ytickers:

        ms = yf.Ticker(tick)

        dataset_train = ms.history(start="2017-01-01", end="2020-11-27")
        dataset_train.drop(['Dividends', 'Stock Splits'], axis=1)
        dataset_train.reset_index(inplace=True)

        cols = list(dataset_train)[1:6]

        #%%time
        # Extract dates (will be used in visualization)
        datelist_train = list(dataset_train['Date'])
        #datelist_train = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in datelist_train]

        dataset_train = dataset_train[cols].astype(str)
        for i in cols:
            for j in range(0, len(dataset_train)):
                dataset_train[i][j] = dataset_train[i][j].replace(',', '')

        dataset_train = dataset_train.astype(float)

        # Using multiple features (predictors)
        training_set = dataset_train.to_numpy()

        # Feature Scaling
        sc = StandardScaler()
        training_set_scaled = sc.fit_transform(training_set)

        sc_predict = StandardScaler()
        sc_predict.fit_transform(training_set[:, 0:1])

        # Creating a data structure with 90 timestamps and 1 output
        X_train = []
        y_train = []

        n_future = 30   # Number of days we want top predict into the future
        n_past = 90    # Number of past days we want to use to predict the future

        for i in range(n_past, len(training_set_scaled) - n_future +1):
            X_train.append(training_set_scaled[i - n_past:i, 0:dataset_train.shape[1] - 1])
            y_train.append(training_set_scaled[i + n_future - 1:i + n_future, 0])

        X_train, y_train = np.array(X_train), np.array(y_train)
        # Initializing the Neural Network based on LSTM
        model = Sequential()

        # Adding 1st LSTM layer
        model.add(LSTM(units=64, return_sequences=True, input_shape=(n_past, dataset_train.shape[1]-1)))

        # Adding 2nd LSTM layer
        model.add(LSTM(units=10, return_sequences=False))

        # Adding Dropout
        model.add(Dropout(0.25))

        # Output layer
        model.add(Dense(units=1, activation='linear'))

        # Compiling the Neural Network
        model.compile(optimizer = Adam(learning_rate=0.01), loss='mean_squared_error')

        #%%time
        es = EarlyStopping(monitor='val_loss', min_delta=1e-10, patience=10, verbose=1)
        rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1)
        mcp = ModelCheckpoint(filepath='weights.h5', monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=True)

        tb = TensorBoard('logs')

        history = model.fit(X_train, y_train, shuffle=True, epochs=30, callbacks=[es, rlr, mcp, tb], validation_split=0.2, verbose=1, batch_size=256)
        # Generate list of sequence of days for predictions
        datelist_future = pd.date_range(datelist_train[-1], periods=n_future, freq='1d').tolist()


        # Convert Pandas Timestamp to Datetime object (for transformation) --> FUTURE
        datelist_future_ = []
        for this_timestamp in datelist_future:
            datelist_future_.append(this_timestamp.date())

        # Perform predictions
        predictions_future = model.predict(X_train[-n_future:])

        predictions_train = model.predict(X_train[n_past:])

        # Inverse the predictions to original measurements



        y_pred_future = sc_predict.inverse_transform(predictions_future)
        y_pred_train = sc_predict.inverse_transform(predictions_train)

        PREDICTIONS_FUTURE = pd.DataFrame(y_pred_future, columns=['Open']).set_index(pd.Series(datelist_future))
        PREDICTION_TRAIN = pd.DataFrame(y_pred_train, columns=['Open']).set_index(pd.Series(datelist_train[2 * n_past + n_future -1:]))
        # Convert <datetime.date> to <Timestamp> for PREDCITION_TRAIN
        PREDICTION_TRAIN.index = PREDICTION_TRAIN.index.to_series().apply(datetime_to_timestamp)

        #PREDICTION_TRAIN.head(3)
        DF_pred.append(PREDICTIONS_FUTURE)

    resData = {}
    for i in range(0, len(DF_pred)):
        resData[ytickers[i]] = DF_pred[i].to_json()
    js_obj = json.dumps(resData, indent=4)
    fl = 'datafile.json'
    if os.path.exists(fl):
        os.remove(fl)
    fileobj = open(fl, 'w')
    fileobj.write(js_obj)
    fileobj.close()
