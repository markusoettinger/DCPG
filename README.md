# DCPG

This is a repository for a simulated distributed energy charging system.

## Motivation

In order to maximize the energy a charging point can deliver, a method for peak-shaving was implemented by a third party. This method relies on information about the time a car is going to be parked at a charging point, so that cars with the earliest deadline can be charged first. To get this Information this System tries to increase User engagement via incentives stored and distributed with a blockchain. 

These are our first steps into the wondrous world of blockchain.

## Basics

The plan is to use w3.py to mange accounts and interact with the "Volta"-Testchain and distribute incentive "tokens".

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