from os import P_NOWAIT
import time

import pandas as pd

import parse_csv
from Web3Library_web import W3Library

df_app, df_server = parse_csv.run()
simEnd = df_server.index.max()

# connect to Blockchain and set defaultAccount to faucet account
instance = W3Library()
# web3 = connect(True)
# # connect to SmartContract
# contract = connectContract(web3)
contract = instance.contract

simTimestamp = df_app.index.min() - pd.Timedelta(minutes=20)

# Timefactor maps total csv Timedelta to a simulationtime of 24 hours
timefactor = 4 / ((df_app.index.max() - simTimestamp).total_seconds() / 3600)

nextTimestamp = [0, 0, simTimestamp + pd.Timedelta(minutes=10)]
server_iterator = df_server.iterrows()
app_iterator = df_app.iterrows()

next_app_query = next(app_iterator)
next_server_query = next(server_iterator)

while 1:

    # sleep till next tim
    ## lass zeit laufen und wenn einer der beiden timestamps erreicht wird dann ->
    

    wakeupttime = check_earlier(nextapp, next_server)
    duration = wakeupttime-no

    if time since last in charging update > x:
        print(whos charing)
        timeof last charging update = now
    
    if duration>0
        if duration > 10:
            duration -=10
            sleep(10)
            continue
        else 
            sleep(duration)



    if next_app_query[0]>next_server_query[0]:
        # do server
        try:
            next_server_query = next(server_iterator)
        except StopIteration:
            break
    else:
        # do app
        try:
            next_app_query = next(app_iterator)
        except StopIteration:
            pass
    

while simTimestamp < simEnd:
    loopstart = time.time()

    if simTimestamp in df_app.index:
        # User App gets new charging process and transacts this charging process to the smart contract
        processes = df_app.loc[simTimestamp]
        for process in processes:
            instance.newAccount(process.userID)
            value, transactionHash = instance.startCharging(userId=process.userID, chargerId=process.Station_ID,
                                                            startTime=process.name,
                                                            estimateDuration=process["ChargingTime[mins]"],
                                                            desiredkWh=process["DesiredkWh[kWh]"])

    if simTimestamp == nextTimestamp[2]:
        # calling contact charging information to update SmartCharging process
        processes = instance.inCharging()
        nextTimestamp[2] = simTimestamp + pd.Timedelta(minutes=10)

    if simTimestamp in df_server.index:
        # Server is receiving stopped charging signal from charging-Station and activates stopCharging function
        # contract payments to Flexibility customers
        processes = df_server.loc[simTimestamp]
        for process in processes:
            transactionHash = instance.stopCharging(userId=process.iat[0, 0], endTime=process.iat[0, 2],
                                                    flexFlow=process.iat[0, 4], chargedkWh=process.iat[0, 3])

    nextTimestamp[0] = df_app[df_app.index > simTimestamp].index.min()
    nextTimestamp[1] = df_app[df_server.index > simTimestamp].index.min()

    looptime = time.time() - loopstart
    sleeptime = ((min(nextTimestamp) - simTimestamp).total_seconds()) * timefactor - looptime
    if sleeptime > 0:
        time.sleep(sleeptime)
    simTimestamp = min(nextTimestamp)
