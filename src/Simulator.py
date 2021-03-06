import time

import pandas as pd
import parse_csv
from Web3Library_sim import W3Library

df_app, df_server = parse_csv.run()
simEnd = df_server.index.max()

server_iterator = df_server.iterrows()
app_iterator = df_app.iterrows()

next_app_query = next(app_iterator)
next_server_query = next(server_iterator)

# connect to Blockchain, SmartContract and set defaultAccount to faucet account
instance = W3Library()

simTimestamp = next_app_query[0] - pd.Timedelta(minutes=20)

# Timefactor maps total csv Timedelta to a simulationtime of 24 hours
timefactor = 0.4 / ((df_app.index.max() - simTimestamp).total_seconds() / 3600)

nextTimestamp = [
    next_app_query[0],
    next_server_query[0],
    simTimestamp + pd.Timedelta(minutes=10),
]
somethingChanged = True

while True:
    loopstart = time.time()

    if simTimestamp == next_app_query[0]:
        # User App gets new charging process and transacts this charging process to the smart contract
        process = next_app_query[1]
        instance.newAccount(process.userID)
        value, transactionHash = instance.startCharging(
            userId=process.userID,
            chargerId=process.Station_ID,
            startTime=process.name,
            estimateDuration=process["ChargingTime[mins]"],
            desiredkWh=process["DesiredkWh[kWh]"],
        )
        try:
            somethingChanged = True
            next_app_query = next(app_iterator)
            nextTimestamp[0] = next_app_query[0]
        except StopIteration:
            pass

    if simTimestamp == next_server_query[0]:
        # Server is receiving stopped charging signal from charging-Station and activates stopCharging function
        # contract payments to Flexibility customers
        process = next_server_query[1]
        transactionHash = instance.stopCharging(
            userId=process.userID,
            chargerId=process.Station_ID,
            endTime=next_server_query[0],
            flexFlow=process["Flex[kWh]"],
            chargedkWh=process["kWhDelivered[kWh]"],
        )
        try:
            somethingChanged = True

            next_server_query = next(server_iterator)
            nextTimestamp[1] = next_server_query[0]
        except StopIteration:
            break

    if simTimestamp == nextTimestamp[2]:
        # print(f"It is {simTimestamp} in Sim Time")
        # calling contact charging information to update SmartCharging process
        nextTimestamp[2] = simTimestamp + pd.Timedelta(minutes=10)
        if somethingChanged:
            instance.inCharging(simTimestamp)
            somethingChanged = False

    looptime = time.time() - loopstart
    sleeptime = (
        (min(nextTimestamp) - simTimestamp).total_seconds()
    ) * timefactor - looptime
    # if sleeptime > 0:
    #     time.sleep(sleeptime)
    simTimestamp = min(nextTimestamp)
instance.endSim()
