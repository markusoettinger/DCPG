# DCPG

This is a repository for a simulated distributed energy charging system.

## Motivation

In order to maximize the energy a charging point can deliver, a method for peak-shaving was implemented by a third party. This method relies on information about the time a car is going to be parked at a charging point, so that cars with the earliest deadline can be charged first. To get this Information this System tries to increase User engagement via incentives stored and distributed with a blockchain. 

These are our first steps into the wondrous world of blockchain.

## Basics

We use Ganache (local Tool: https://www.trufflesuite.com/ganache) to set up a local blockchain which is manageble
through web3.py. 

## Setup

```
conda env create -f environment.yml
```

```
activate dcpg
```
Setting up Ganache with contracts from Trufflesuit
* install Ganache from https://www.trufflesuite.com/ganache
* install truffle using :```npm install -g truffle```
* setup ganache server with adding project by selecting truffle-config.js in the MetaCoin folder
* move to MetaCoin folder in the terminal
* deploy contracts using: ```truffle migrate```
* redeploying contracts using ```truffle migrate --reset```

## Test

No real tests yet, but run:

```
pytest
```


## Format Python

To align formating the formater "Black" is used for all Python files. Please format your files before committing.



## Setting up the Frontend

Setting Up Ganache:
* Make sure that you have set up ganache like explained above in section "setup"
* Make sure the ganache server is running

Setting up Node.js:
* Make sure that node.js is installed. If not you can download it here https://nodejs.org/en/.

Starting FastAPI:
* Start a command prompt and activate the virtual environment by typing in "activate DCPG"
* Navigate to the directory "DCPG/src" and start the webapi.py file with the command "python.py"

Starting the Frontend:
* Open up another command prompt and navigate to the directory "DCPG/frontend"
* Initialize the node,js with the command "npm -i"
* After node.js has been initialized you can start the frontend with the command "npm start"
* If the frontend doesn't start automatically in your browser, you can type in the adress http://localhost:8080 manually

