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

First of all you have to make sure that your ganache server is running. If this is the case, you can start setting up the frontend.
For setting up the frontend you need node.js which you can download from https://nodejs.org/en/.
After that, you have to make sure that the FastAPI script is running. For that, start the virtual environment with the command "activate DCPG". Then navigate through your command prompt to the directory DCPG/src and start the wepapi.py file with the command "python wepapi.py".
Next, you will need to navigate to the directory DCPG/frontend and initialize the node.js with the command "npm -i".
Then, you can type the command "npm start". The frontend should open now in your browser with the adress http://localhost:8080. If not,
you can type in the adress manually in your browser.
