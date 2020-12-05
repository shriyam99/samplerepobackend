import yfinance as yf
import numpy as np
import json
import pandas as pd
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

from datetime import date

Tickers = []

with open('allTickers.txt', 'r') as fp:
    lines = fp.readlines()
    for line in lines:
        current_place = line[:-1]
        if (current_place != ""):
            Tickers.append(current_place)


to = date.today()
to = str(to)
#to = to[8]+to[9]+"/"+to[5]+to[6]+"/"+to[0]+to[1]+to[2]+to[3]

def datetime_to_timestamp(x):
    '''
        x : a given datetime value (datetime.date)
    '''
    return datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')


DF_pred = []
DF_train = []
for tick in Tickers:
    ms = yf.Ticker(tick)

    dataset_train = ms.history(start="2017-01-01", end=to)
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
    n_past = 200    # Number of past days we want to use to predict the future

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


    DF_train.append(PREDICTION_TRAIN)
    DF_pred.append(PREDICTIONS_FUTURE)


for i in range(0, len(DF_pred)):
    # resData.add(str(tickers[i]), str(DF_pred[i]))
    print(Tickers[i])
    print("\n\n")
    print(DF_pred[i])
    print("\n")
    print("-"*45)

rmls = []
for j in range(0, len(DF_pred)):
    ckval = (DF_train[j].tail(1))['Open'][0]

    sr = DF_pred[j]['Open'][(DF_pred[j]['Open']) < (0.75*ckval)]

    if(sr.count() >= 1):
        rmls.append(j)


print("Remove index list is:")
print(rmls)

dict = {}
for i in range(0, len(DF_pred)):
    if i not in rmls:
        js = DF_pred[i].to_json()
        dict[Tickers[i]] = js

ls2= []
for j in rmls:
    ls2.append(Tickers[j])

dict2 = {'data' : ls2}

with open("Stockinloss.json", "w") as fo:
    js_obj = json.dumps(dict2, indent=4)
    fo.write(js_obj)

with open("tableData.json", "w") as fileobj:
    js_obj = json.dumps(dict, indent=4)
    print(js_obj)
    fileobj.write(js_obj)
