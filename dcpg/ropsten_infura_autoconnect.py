InfuraProjectId = '1761beb5aae7459b83afd64e8f1003fc'

import os

os.environ['WEB3_INFURA_PROJECT_ID'] = InfuraProjectId

from web3.auto.infura import w3
print(w3.isConnected())