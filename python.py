import yfinance as yf
# import numpy as np
import sys
import asyncio
import pandas as pd
# import glob
import requests
import os
import json
import csv

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

    for i in cal:
        if(i == "Bullish"):
            ans+=1
    cmpName = cmpName + ".NS"
    df[cmpName] = ans

sort_orders = sorted(df.items(), key=lambda x: x[1], reverse=True)

for i in sort_orders:
	print(i[0], i[1])


f.close()
s.close()
