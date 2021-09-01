import requests, json, time, threading
from web3 import Web3
from web3.middleware import geth_poa_middleware
import datetime

appURL = ''
infuraProvider = ''
w3 = ''

ABACOpt5Addr = '0xF022657BFd61C1F48e00413Ad2F5038dFB0EEA53'

ABACOpt5rawJSON = '''[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "start",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "end",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256[]",
          "name": "idx",
          "type": "uint256[]"
        },
        {
          "indexed": false,
          "internalType": "bytes32[]",
          "name": "userId",
          "type": "bytes32[]"
        },
        {
          "indexed": false,
          "internalType": "bytes32[]",
          "name": "objectId",
          "type": "bytes32[]"
        },
        {
          "indexed": false,
          "internalType": "bytes32[]",
          "name": "operation",
          "type": "bytes32[]"
        },
        {
          "indexed": false,
          "internalType": "bool[]",
          "name": "response",
          "type": "bool[]"
        }
      ],
      "name": "accessMultipleResponse",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "userId",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "objectId",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "operation",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "bool",
          "name": "accessGiven",
          "type": "bool"
        }
      ],
      "name": "accessRequestResponse",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "userId",
          "type": "bytes32"
        },
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "operation",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "bytes32[]",
          "name": "objects",
          "type": "bytes32[]"
        }
      ],
      "name": "accessibleObjectsReturned",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "functName",
          "type": "bytes32"
        }
      ],
      "name": "functionAccessed",
      "type": "event"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_U",
          "type": "bytes32[]"
        }
      ],
      "name": "addUsers",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_UA",
          "type": "bytes32[]"
        }
      ],
      "name": "addUserAttributes",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_UA",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_value",
          "type": "bytes32[]"
        }
      ],
      "name": "addUserAttributePosValues",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_U",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_attr",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_value",
          "type": "bytes32[]"
        }
      ],
      "name": "addUserAttributeValuePair",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getUsers",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getUserAttributes",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_UA",
          "type": "bytes32"
        }
      ],
      "name": "getUserAttributePosValues",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_U",
          "type": "bytes32"
        }
      ],
      "name": "getUserAttributeValuePair",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_O",
          "type": "bytes32[]"
        }
      ],
      "name": "addObjects",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_OA",
          "type": "bytes32[]"
        }
      ],
      "name": "addObjectAttributes",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_OA",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_value",
          "type": "bytes32[]"
        }
      ],
      "name": "addObjectAttributePosValues",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_O",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_attr",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_value",
          "type": "bytes32[]"
        }
      ],
      "name": "addObjectAttributeValuePair",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getObjects",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getObjectAttributes",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_OA",
          "type": "bytes32"
        }
      ],
      "name": "getObjectAttributePosValues",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_O",
          "type": "bytes32"
        }
      ],
      "name": "getObjectAttributeValuePair",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_OP",
          "type": "bytes32[]"
        }
      ],
      "name": "addOperations",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getOperations",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_rules",
          "type": "bytes32[]"
        }
      ],
      "name": "addRules",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_attr",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_val",
          "type": "bytes32[]"
        }
      ],
      "name": "addUserAttributeValuePairToRule",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_attr",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_val",
          "type": "bytes32[]"
        }
      ],
      "name": "addObjectAttributeValuePairToRule",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "_op",
          "type": "bytes32"
        }
      ],
      "name": "addOperationToRule",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getRules",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        }
      ],
      "name": "getUserAttributeValuePairFromRule",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        }
      ],
      "name": "getObjectAttributeValuePairFromRule",
      "outputs": [
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_ruleId",
          "type": "bytes32"
        }
      ],
      "name": "getOperationFromRule",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_userId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "_objectId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "_operation",
          "type": "bytes32"
        },
        {
          "internalType": "bool",
          "name": "_accessGiven",
          "type": "bool"
        }
      ],
      "name": "accessRequestPerObject",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_userId",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "_operation",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32[]",
          "name": "_objects",
          "type": "bytes32[]"
        }
      ],
      "name": "getAccessibleObjects",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_start",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_end",
          "type": "uint256"
        },
        {
          "internalType": "uint256[]",
          "name": "_idx",
          "type": "uint256[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_userId",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_objectId",
          "type": "bytes32[]"
        },
        {
          "internalType": "bytes32[]",
          "name": "_operation",
          "type": "bytes32[]"
        },
        {
          "internalType": "bool[]",
          "name": "_response",
          "type": "bool[]"
        }
      ],
      "name": "getMultipleResponse",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
'''

ABACOpt5ABI = json.loads(ABACOpt5rawJSON)
ABACOpt5Contract = ""

ABACContract = ABACOpt5Contract
ABACContractAddr = ABACOpt5Addr

def setAppURL(_url):
    global appURL
    print(appURL)
    appURL =  _url

def setInfuraId(_id):
    global infuraProvider, w3
    infuraProvider =  'https://rinkeby.infura.io/v3/' + str(_id)
    w3 = Web3(Web3.HTTPProvider(infuraProvider))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    setSmartContractAddr(ABACContractAddr)

def setSmartContractAddr(_addr):
    global ABACOpt5Addr, ABACOpt5Contract, ABACContractAddr, ABACContract
    ABACOpt5Addr = _addr
    ABACOpt5Contract = w3.eth.contract(address=ABACOpt5Addr, abi=ABACOpt5ABI)
    ABACContractAddr = ABACOpt5Addr
    ABACContract = ABACOpt5Contract

def setSmartContractABI(_abi):
    global ABACOpt5rawJSON, ABACOpt5ABI, ABACOpt5Contract
    ABACOpt5rawJSON = _abi
    ABACOpt5ABI = json.loads(ABACOpt5rawJSON)
    ABACOpt5Contract = w3.eth.contract(address=ABACOpt5Addr, abi=ABACOpt5ABI)
    ABACContractAddr = ABACOpt5Addr
    ABACContract = ABACOpt5Contract