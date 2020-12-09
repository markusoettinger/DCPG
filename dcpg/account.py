# %%

from web3 import Web3

#%%

weby = Web3(Web3.HTTPProvider("https://volta-rpc.energyweb.org"))

#%%

acc = weby.eth.account.create("this is a very long and cool string")
# %%
