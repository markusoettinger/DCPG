from Web3Library import *
import parse_csv
import pandas as pd
import time

df_app_csv, df_server_csv = parse_csv.run()
simEnd = df_app_csv.index.max()

# connect to Blockchain and set defaultAccount to faucet account
web3 = connect(True)
# connect to SmartContract
contract = connectContract(web3)
# initialize account list
df_accounts = pd.DataFrame([], columns=["userID", "Address"])

simTimestamp = df_app_csv.index.min() - pd.Timedelta(minutes=20)
simStart = [[pd.Timestamp.today(), simTimestamp, 'Simulation Start', '-', '-', '-']]
columns = ["Timestamp", "SimTimestamp", "Eventtype", "userID", "Hash", "Value"]

simLog = pd.DataFrame(simStart, columns=columns)

# Timefactor maps total csv Timedelta to a simulationtime of 24 hours
timefactor = 24 / ((df_app_csv.index.max() - simTimestamp).total_seconds() / 3600)

nextTimestamp = [0, 0, simTimestamp + pd.Timedelta(minutes=10)]

while simTimestamp < simEnd:
    loopstart = time.time()

    if simTimestamp in df_app_csv.index:
        # User App gets new charging process and transacts this charging process to the smart contract
        process = df_app_csv.loc[simTimestamp]
        if process.userID not in df_accounts.userID:
            web3, newAddress, df_accounts = newAccount(web3, process.userID, df_accounts)
            simLog = simLog.append({"Timestamp": pd.Timestamp.today(),
                                    "SimTimestamp": simTimestamp,
                                    "Eventtype": 'Create Account',
                                    "userID": process.userID,
                                    "Value": 1000}, ignore_index=True)
        value, transactionHash = startCharging(web3, contract, df_accounts, process.userID, process.Station_ID,
                                               process.name, process["ChargingTime[mins]"],
                                               process["DesiredkWh[kWh]"])
        simLog = simLog.append({"Timestamp": pd.Timestamp.today(),
                                "SimTimestamp": simTimestamp,
                                "Eventtype": 'StartCharging',
                                "userID": process.userID,
                                "Hash": transactionHash,
                                "Value": value}, ignore_index=True)

    if simTimestamp in df_server_csv.endtime:
        # Server is receiving stopped charging signal from charging-Station and activates stopCharging function
        # contract payments to Flexibility customers
        process = df_server_csv[df_server_csv.endtime == simTimestamp]
        transactionHash = stopCharging(web3, contract, df_accounts, process.userID, process.Station_ID, process.endtime,
                                        process["Flex[kWh]"], process["kWhDelivered[kWh]"])
        simLog = simLog.append({"Timestamp": pd.Timestamp.today(),
                                "SimTimestamp": simTimestamp,
                                "Eventtype": 'StopCharging',
                                "userID": process.userID,
                                "Hash": transactionHash,
                                "Value": process["Flex[kWh]"]}, ignore_index=True)

    if simTimestamp == nextTimestamp[2]:
        # calling contact charging information to update SmartCharging process
        # call_inCharging()
        nextTimestamp[2] = simTimestamp + pd.Timedelta(minutes=10)

    nextTimestamp[0] = df_app_csv[df_app_csv.index > simTimestamp].index.min()
    nextTimestamp[1] = df_server_csv[df_server_csv["endtime"] > simTimestamp]["endtime"].min()

    looptime = time.time() - loopstart
    sleeptime = ((min(nextTimestamp) - simTimestamp).total_seconds()) * timefactor - looptime
    if sleeptime > 0:
        time.sleep(sleeptime)
    simTimestamp = min(nextTimestamp)

simLog = simLog.set_index("Timestamp")
simLog.to_csv('Simulation_Log.csv')
