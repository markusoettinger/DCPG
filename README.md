# DCPG

This is a repository for a simulated distributed energy charging system.

## Motivation

In order to maximize the energy a charging point can deliver, a method for peak-shaving was implemented by a third party. This method relies on information about the time a car is going to be parked at a charging point, so that cars with the earliest deadline can be charged first. To get this Information this System tries to increase User engagement via incentives stored and distributed with a blockchain. 

These are our first steps into the wondrous world of blockchain.

## Basics

The plan is to use w3.py to mange accounts and interact with the "Volta"-Testchain and distribute incentive "tokens".

That plan may very due to the fact, that connecting to the Volta-RPC is pure shit and we were'nt be able to make transactions...
Therefore we use Ganache (local Tool: https://www.trufflesuite.com/ganache) to set up a local blockchain which is manageble
through web3.py. 

## Setup

```
conda env create -f environment.yml
```

```
activate dcpg
```

## Test

No real tests yet, but run:

```
pytest
```

## Format Python

To align formating the formater "Black" is used for all Python files. Please format your files before committing.



## reminder to add frontend setup