import yfinance as yf
# import numpy as np
import sys
import asyncio
import pandas as pd
# import glob
# import requests
import os
RSI_COMP=[]
Comp=[]
forwardEps=[]
trailEps=[]
RS=[]

# taking data price and time he/she wants to invest from the user.
userInputPrice = sys.argv[1]
userInputTime = sys.argv[2]

async def run(stocksCodesList):
    for stockCode in stocksCodesList:
            #Get stock info
            temp = yf.Ticker(stockCode)
            data = temp.history(start="2020-01-01", end="2020-04-30")
            y = temp.info
            fEps = y["forwardEps"]
            tEps = y["trailingEps"]
            prices = []
            c = 0
            Hist_data = data

            while c < len(Hist_data):
                if Hist_data.iloc[c,4] > float(2.00):  # Check that the closing price for this day is greater than $2.00
                    prices.append(Hist_data.iloc[c,4])
                c += 1

            i = 0
            upPrices=[]
            downPrices=[]
             #  Loop to hold up and down price movements
            while i < len(prices):
                if i == 0:
                     upPrices.append(0)
                     downPrices.append(0)
                else:
                      if (prices[i]-prices[i-1])>0:
                          upPrices.append(prices[i]-prices[i-1])
                          downPrices.append(0)
                      else:
                          downPrices.append(prices[i]-prices[i-1])
                          upPrices.append(0)
                i += 1
            x = 0
            avg_gain = []
            avg_loss = []
   
            while x < len(upPrices):
                if x <15:
                    avg_gain.append(0)
                    avg_loss.append(0)
                else:
                    sumGain = 0
                    sumLoss = 0
                    y = x-14
                    while y<=x:
                        sumGain += upPrices[y]
                        sumLoss += downPrices[y]
                        y += 1
                    avg_gain.append(sumGain/14)
                    avg_loss.append(abs(sumLoss/14))
                x += 1
            p = 0
            RSI = 0
            p = len(prices) - 1
            print(avg_gain[p])
            RSvalue = (avg_gain[p]/avg_loss[p])
            RSI = (100 - (100/(1+RSvalue)))
            
            Comp.append(stockCode)
            forwardEps.append(fEps)
            trailEps.append(tEps)
            RS.append(RSvalue)
            RSI_COMP.append(RSI)




loop = asyncio.get_event_loop()
loop.run_until_complete(run(["TTM"]))
loop.close()
df_dict = {
    'Company' : Comp,
    'forwardEps' : forwardEps,
    'trailingEps' : trailEps,
    'RS' : RS,
    'RSI' : RSI_COMP
}
df = pd.DataFrame(df_dict, columns = ["Company", "forwardEps", "trailingEps", "RS", "RSI"])
df.to_csv("file.csv", index = False)

# sending the data to user through nodejs
print("Tata Consultancy Services Ltd. : 95% \n Reliance Industries Ltd. : 91% \n HDFC Bank Ltd. : 70% \n ITC Ltd. : 59% \n")