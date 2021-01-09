import logging as log
from datetime import datetime

from web3 import Web3, HTTPProvider

t = "%d-%m-%Y%H-%M-%S"

contractaddress = '0x839C63be21bAb1218db533af4267179CBf31d3cc'
contractabi = '[    {      "inputs": [        {          "internalType": "string",          "name": "station",          "type": "string"        }      ],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "name": "chargingprocesses",      "outputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "address",          "name": "chargee",          "type": "address"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "availableFlex",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "godwin",      "outputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "getChargingProcessesLength",      "outputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [],      "name": "loadGasBuffer",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "endTime",          "type": "uint256"        },        {          "internalType": "int256",          "name": "flexFlow",          "type": "int256"        },        {          "internalType": "uint256",          "name": "chargedWh",          "type": "uint256"        }      ],      "name": "stopCharging",      "outputs": [],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "name": "startCharging",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    }  ]'
# dies if logs folder is missing
log.basicConfig(level=log.INFO, format="%(asctime)s %(message)s", handlers= [log.FileHandler(f'../logs/{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log'), log.StreamHandler()])


class W3Library:
    def __init__(self, should_log=False):
        log.info(f"[StartSim] Simulation started")
        self.web3 = self.connect()
        self.contract = self.connectContract()
        self.accounts = {}
        self.contract.functions.loadGasBuffer().transact({'value': int(100 * 1e18)})
        log.info(f"[ContrCon] Loaded GasBuffer of the SmartContract with 100 ether")

    def connect(self, rpc_server='HTTP://127.0.0.1:7545'):
        try:
            web3 = Web3(HTTPProvider(rpc_server))
            if not web3:
                raise Exception
            web3.eth.defaultAccount = web3.eth.accounts[0]
            log.info(f"[Connect ] connected to rpc-server: {rpc_server}")
            log.info(f"[DefAcc  ] Default account: {web3.eth.accounts[0]}")
            return web3
        except Exception as e:
            print("Error connecting")
            log.info(f"[Error   ] Error connecting")
            return False

    def connectContract(self):
        log.info(f"[ContrCon] Connected to SmartContract with address: {contractaddress}")
        return self.web3.eth.contract(address=self.web3.toChecksumAddress(contractaddress), abi=contractabi)

    def getBalance(self, address):
        return self.web3.eth.getBalance(address)

    def getBalanceForUser(self, userId):
        if userId in self.accounts:
            return self.web3.eth.getBalance(self.accounts[userId]["address"])
        raise IndexError("[Error   ] UserId not known in Accounts")

    def transact(self, toAddress, fromAddress, value):
        value = int(value)
        if fromAddress == 'Faucet':
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'value': value})
        else:
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'from': fromAddress, 'value': value})
        log.info(
            f"[Transact] Transaction of {value * 1e-18} ether from {fromAddress} to {toAddress}")
        return Web3.toHex(ret)

    def newAccount(self, userId):
        # df_accounts = pd.readcsv('accountList.csv')
        if userId not in self.accounts:
            newAddress = self.web3.geth.personal.new_account(str(userId))
            self.web3.geth.personal.unlockAccount(newAddress, str(userId), 0)
            self.accounts[userId] = {'userID': userId, 'address': newAddress, "chargerId": None, "retainingTokens": None}
            log.info(f"[NewAcc  ] New account {newAddress} created for user {userId}")
            # FaucetTransaction
            self.transact(newAddress, 'Faucet', 3e20)  # need to be changed to highest Flexpayer amount

            return newAddress
        return

    def startCharging(self, userId, chargerId, startTime, estimateDuration, desiredkWh, flex=None):
        P_charger = 3.5  # kW --> example for calculating max Flex to pay
        # estimateDuration evtl. umwandeln
        fromAddress = self.accounts[userId]["address"]
        self.accounts[userId]["chargerId"] = chargerId
        av_balance = self.getBalance(fromAddress)
        # Check balance for amount available
        if flex is None:
            flexWh = desiredkWh - (P_charger * (estimateDuration.total_seconds() / 3600)) + 10
            flex = int(flexWh * 1e18)
        if flex > av_balance:
            flex = av_balance
        if flex < 0:
            flex = 0
        self.accounts[userId]["retainingTokens"] = flex * 1e-18
        desiredWh = int(desiredkWh * 1000)
        try:
            transactionHash = self.contract.functions.startCharging(userId, chargerId, int(startTime.timestamp()),
                                                                    int(round(estimateDuration.total_seconds(), 0)),
                                                                    desiredWh).transact(
                {'from': fromAddress, 'value': flex})
        except ValueError:
            log.info(f"[LowFunds] User {userId} doesn't have enough founds to send {round(flex*1e-18,3)} ether. Current account balance: {round(self.getBalance(fromAddress) * 1e-18, 3)} ether ")
            self.transact(fromAddress, 'Faucet', 3e20)
            log.info(f"[NewBal  ] User {userId} recharged it's account with 300 ether due to insufficient balance for transaction")
            transactionHash = self.contract.functions.startCharging(userId, chargerId, int(startTime.timestamp()),
                                                                    int(round(estimateDuration.total_seconds(), 0)),
                                                                    desiredWh).transact(
                {'from': fromAddress, 'value': flex})
        self.web3.eth.waitForTransactionReceipt(transactionHash)
        log.info(
            f"[StrtChar] User {userId} started charging at {chargerId} and payed {round(flex * 1e-18, 3)} to the contract. Simulation Time: {str(startTime)}")
        return flex, transactionHash

    def stopCharging(self, userId, endTime, flexFlow, chargedkWh):
        for i in range(1):
            try:
                chargedWh = int(chargedkWh * 1000)
                flexFlow = int(flexFlow * 1e18)
                oldBalance = self.getBalance(self.accounts[userId]["address"])
                transactionHash = self.contract.functions.stopCharging(userId, self.accounts[userId]["chargerId"],
                                                                       int(endTime.timestamp()), flexFlow, chargedWh).transact()
                self.web3.eth.waitForTransactionReceipt(transactionHash)
                contract_transaction = (self.getBalance(self.accounts[userId]["address"]) - oldBalance) * 1e-18
                log.info(f"[StopChar] User {userId} stopped charging at {self.accounts[userId]['chargerId']} with flex used: {round(flexFlow* 1e-18,3)} Simulation Time: {str(endTime)}")
                log.info(f"[Transact] Contract transacted {round(contract_transaction, 3)} ether to userID {userId}")
                if abs(self.accounts[userId]["retainingTokens"] - contract_transaction + (flexFlow * 1e-18)) > 0.1:
                    log.info(f"[TransErr] Contract transacted wrong amount of tokens")
                self.accounts[userId]["chargerId"] = None
                self.accounts[userId]["retainingTokens"] = None
                return transactionHash
            except self.web3.exceptions.SolidityError:
                self.contract.functions.loadGasBuffer().transact({'value': int(100 * 1e18)})
                log.info(f"[ContrCon] Loaded GasBuffer of the SmartContract with 100 ether")
                continue
        raise ConnectionError(f"Still got Error at Stop Charging userID {userId}. Flex: {round(flexFlow* 1e-18,3)}")

    def inCharging(self):
        numberCharging = self.contract.functions.getChargingProcessesLength().call()
        processes = []
        log.info(
            f"[CharInfo] Currently are {numberCharging} charging processes active. Contract Balance: {round(self.getBalance(contractaddress) * 1e-18, 3)} ether")
        varNames = ["userID", "chargerID", "chargee", "startTime", "estimatedDuration", "availableFlex", "desiredWh"]
        for i in range(numberCharging):
            process = self.contract.functions.chargingprocesses(i).call()
            processes.append(dict(zip(varNames, process)))
        return processes
