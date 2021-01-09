import time

import pandas as pd

import parse_csv
from Web3Library_web import W3Library

df_app_csv, df_server_csv = parse_csv.run()
simEnd = df_server_csv.index.max()

# connect to Blockchain and set defaultAccount to faucet account
instance = W3Library()
# web3 = connect(True)
# # connect to SmartContract
# contract = connectContract(web3)
contract = instance.contract

simTimestamp = df_app_csv.index.min() - pd.Timedelta(minutes=20)

# Timefactor maps total csv Timedelta to a simulationtime of 24 hours
timefactor = 4 / ((df_app_csv.index.max() - simTimestamp).total_seconds() / 3600)

nextTimestamp = [0, 0, simTimestamp + pd.Timedelta(minutes=10)]

while simTimestamp < simEnd:
    loopstart = time.time()

    if simTimestamp in df_app_csv.index:
        # User App gets new charging process and transacts this charging process to the smart contract
        processes = df_app_csv.loc[simTimestamp]
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

    if simTimestamp in df_server_csv.index:
        # Server is receiving stopped charging signal from charging-Station and activates stopCharging function
        # contract payments to Flexibility customers
        processes = df_server_csv.loc[simTimestamp]
        for process in processes:
            transactionHash = instance.stopCharging(userId=process.iat[0, 0], endTime=process.iat[0, 2],
                                                    flexFlow=process.iat[0, 4], chargedkWh=process.iat[0, 3])

    nextTimestamp[0] = df_app_csv[df_app_csv.index > simTimestamp].index.min()
    nextTimestamp[1] = df_app_csv[df_server_csv.index > simTimestamp].index.min()

    looptime = time.time() - loopstart
    sleeptime = ((min(nextTimestamp) - simTimestamp).total_seconds()) * timefactor - looptime
    if sleeptime > 0:
        time.sleep(sleeptime)
    simTimestamp = min(nextTimestamp)
