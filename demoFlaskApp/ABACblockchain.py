import json
from web3 import Web3
from datetime import datetime
from web3.middleware import geth_poa_middleware
from flask import flash
from threading import Thread, Lock

### General info
infuraId = ''   ## get your infura id and update it here 
infuraProvider = 'https://rinkeby.infura.io/v3/' + str(infuraId)
w3 = Web3(Web3.HTTPProvider(infuraProvider))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

## address and private key of ethereum account used by ABAC application  cloud server to update ABAC state changes in blockchain network
addr1 = '' 
privateKey1 = ''


### various smart contracts used for testing. The most recent one is ABACOpt5
ABACOpt1Addr = '0xbcEe1e6Bf9B03BE8fC05D557536e5e859cB35deD'
ABACOpt2Addr = '0x4E1aA5983866109e034F4Eb76088e396b1E7aDfe'
ABACOpt3Addr = '0x0599B4BBEA0DFAd3Ca3589b371a5A5c18A1B8a5a'
ABACOpt5Addr = '0xF022657BFd61C1F48e00413Ad2F5038dFB0EEA53'

ABACOpt1rawJSON = '''[
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
    }
  ]'''

ABACOpt2rawJSON = '''[
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
    }
  ]'''

ABACOpt3rawJSON = '''[
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
    }
  ]'''

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
  ]'''

ABACOpt1ABI = json.loads(ABACOpt1rawJSON)
ABACOpt2ABI = json.loads(ABACOpt2rawJSON)
ABACOpt3ABI = json.loads(ABACOpt3rawJSON)
ABACOpt5ABI = json.loads(ABACOpt5rawJSON)
ABACOpt1Contract = w3.eth.contract(address=ABACOpt1Addr, abi=ABACOpt1ABI)
ABACOpt2Contract = w3.eth.contract(address=ABACOpt2Addr, abi=ABACOpt2ABI)
ABACOpt3Contract = w3.eth.contract(address=ABACOpt3Addr, abi=ABACOpt3ABI)
ABACOpt5Contract = w3.eth.contract(address=ABACOpt5Addr, abi=ABACOpt5ABI)

ABACContract = ABACOpt5Contract
ABACContractAddr = ABACOpt5Addr

### Common Functions ####
def sendTx(_nonce, _to, _data, _value=0):
    txObject = {'nonce':_nonce, 'gasPrice':Web3.toHex(Web3.toWei('20', 'gwei')), 'gas':Web3.toHex(3000000), 'to':_to, 'value':_value, 'data':_data}
    signedTx = w3.eth.account.signTransaction(txObject, privateKey1)
    txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    return txHash

def fStrtoHex(arr):
    if isinstance(arr, list):
      res = [Web3.toHex(text=x) for x in arr]
    else:
      res = Web3.toHex(text = arr)
    return res

def fHextoStr(arr):
    if isinstance(arr, list):
      res = [Web3.toText(hexstr=x) for x in arr]
    else:
      res = Web3.toText(hexstr=arr)
    return res

def fHexbyteToStr(arr):
    if isinstance(arr, list):
      res = [ x.decode('utf8').rstrip('\x00') for x in arr]
    else:
      res = arr.decode('utf8').rstrip('\x00')
    return res

def getInpFunDetails(input):
    decoded_input = ABACContract.decode_function_input(input)
    funName = str(decoded_input[0]).split()[1].split('(')[0]
    funAttr = decoded_input[1]
    for x in funAttr:
      funAttr[x] = fHexbyteToStr(funAttr[x])
    return funName, funAttr

#### Functions to modify userAttributes
def insertUsersBC(users):
    usersHex = fStrtoHex(users)
    data = ABACContract.encodeABI(fn_name="addUsers", args=[usersHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    txHash = '0x'+txHash.hex() 
    return txHash

def insertUserAttributesBC(attrs):
    attrsHex = fStrtoHex(attrs)
    data = ABACContract.encodeABI(fn_name="addUserAttributes", args=[attrsHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    txHash = '0x'+txHash.hex() 
    return txHash

def insertUserAttributePosValuesBC(attrName, attrValues):
    attrNameHex = Web3.toHex(text=attrName)
    attrValuesHex = fStrtoHex(attrValues)
    data = ABACContract.encodeABI(fn_name="addUserAttributePosValues", args=[attrNameHex, attrValuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def insertUserAttributeValuePairBC(userId, attrs, values):
    userIdHex = Web3.toHex(text=userId)
    attrsHex = fStrtoHex(list(attrs))
    valuesHex = fStrtoHex(list(values))
    data = ABACContract.encodeABI(fn_name="addUserAttributeValuePair", args=[userIdHex,  attrsHex, valuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash


### Functions to modify ObjectAttributes
def insertObjectsBC(objects):
    objectsHex = fStrtoHex(objects)
    data = ABACContract.encodeABI(fn_name="addObjects", args=[objectsHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    txHash = '0x'+txHash.hex() 
    return txHash

def insertObjectAttributesBC(attrs):
    attrsHex = fStrtoHex(attrs)
    data = ABACContract.encodeABI(fn_name="addObjectAttributes", args=[attrsHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    txHash = '0x'+txHash.hex() 
    return txHash

def insertObjectAttributePosValuesBC(attrName, attrValues):
    attrNameHex = Web3.toHex(text=attrName)
    attrValuesHex = fStrtoHex(attrValues)
    data = ABACContract.encodeABI(fn_name="addObjectAttributePosValues", args=[attrNameHex, attrValuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def insertObjectAttributeValuePairBC(objectId, attrs, values):
    objectIdHex = Web3.toHex(text=objectId)
    attrsHex = fStrtoHex(list(attrs))
    valuesHex = fStrtoHex(list(values))
    data = ABACContract.encodeABI(fn_name="addObjectAttributeValuePair", args=[objectIdHex,  attrsHex, valuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

### Function to add operations
def insertOperationsBC(operations):
    operationsHex = fStrtoHex(operations)
    data = ABACContract.encodeABI(fn_name="addOperations", args=[operationsHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    txHash = '0x'+txHash.hex() 
    return txHash   

### Functions to modify Policy rules
def insertUserAttributeValuePairToRuleBC(ruleId, attrs, values):
    ruleIdHex = Web3.toHex(text=ruleId)
    attrsHex = fStrtoHex(list(attrs))
    valuesHex = fStrtoHex(list(values))            
    data = ABACContract.encodeABI(fn_name="addUserAttributeValuePairToRule",args=[ruleIdHex, attrsHex, valuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash
    
def insertObjectAttributeValuePairToRuleBC(ruleId, attrs, values):
    ruleIdHex = Web3.toHex(text=ruleId)
    attrsHex = fStrtoHex(list(attrs))
    valuesHex = fStrtoHex(list(values))          
    data = ABACContract.encodeABI(fn_name="addObjectAttributeValuePairToRule",args=[ruleIdHex, attrsHex, valuesHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def insertOperationToRuleBC(ruleId, operation):
    ruleIdHex = Web3.toHex(text=ruleId)
    operationHex = Web3.toHex(text=operation)
    data = ABACContract.encodeABI(fn_name="addOperationToRule",args=[ruleIdHex,operationHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def insertRulesBC(rules):
    rulesHex = fStrtoHex(rules)
    data = ABACContract.encodeABI(fn_name="addRules",args=[rulesHex])  
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def verifyTransactions(funName, querySet, txCnt=1, noOfBlocks=-1):
    lastBlock = w3.eth.blockNumber
    firstBlock = 0
    print("latest Block : ", lastBlock)
    # flash("latest Block : " + str(lastBlock))

    if noOfBlocks != -1:  
        firstBlock = lastBlock - noOfBlocks
    eventNameHash = w3.keccak(text="functionAccessed(bytes32)").hex()
    funcType = 1
    resTxns = []
   
    if funName == "addUsers":
        funHash = (Web3.toHex(text = "user1") + "0"*64)[:66]
        type1Query = "users"
        type1Input = "_U"
    elif funName == "addUserAttributes":
        funHash = (Web3.toHex(text = "user2") + "0"*64)[:66]
        type1Query = "userAttributes"
        type1Input = "_UA"
    elif funName == "addUserAttributePosValues":
        funHash = (Web3.toHex(text = "user3") + "0"*64)[:66]
        funcType = 2
        type2Query1 = "userAttributeName"
        type2Query2 = "userAttributeValues"
        type2Input = "_UA"
    elif funName == "addUserAttributeValuePair":
        funHash = (Web3.toHex(text = "user4") + "0"*64)[:66]
        funcType = 3
        type3Query1 = "userId"
        type3Query2 = "userAttributeValuePair"
        type3Input = "_U"
    elif funName == "addObjects":
        funHash = (Web3.toHex(text = "object1") + "0"*64)[:66]
        type1Query = "objects"
        type1Input = "_O"
    elif funName == "addObjectAttributes":
        funHash = (Web3.toHex(text = "object2") + "0"*64)[:66]
        type1Query = "objectAttributes"
        type1Input = "_OA"
    elif funName == "addObjectAttributePosValues":
        funHash = (Web3.toHex(text = "object3") + "0"*64)[:66]
        funcType = 2
        type2Query1 = "objectAttributeName"
        type2Query2 = "objectAttributeValues"
        type2Input = "_OA"
    elif funName == "addObjectAttributeValuePair": 
        funHash = (Web3.toHex(text = "object4") + "0"*64)[:66] 
        funcType = 3
        type3Query1 = "objectId"
        type3Query2 = "objectAttributeValuePair"
        type3Input = "_O" 
    elif funName == "addOperations":
        funHash = (Web3.toHex(text = "operation") + "0"*64)[:66]
        type1Query = "operations"
        type1Input = "_OP"
    elif funName == "addRules":
        funHash = (Web3.toHex(text = "rule1") + "0"*64)[:66]
        type1Query = "rules"
        type1Input = "_rules"
    elif funName == "addUserAttributeValuePairToRule":
        funHash = (Web3.toHex(text = "rule2") + "0"*64)[:66]
        funcType = 3
        type3Query1 = "ruleId"
        type3Query2 = "userAttributeValuePair"
        type3Input = "_ruleId" 
    elif funName == "addObjectAttributeValuePairToRule":
        funHash = (Web3.toHex(text = "rule3") + "0"*64)[:66]
        funcType = 3
        type3Query1 = "ruleId"
        type3Query2 = "objectAttributeValuePair"
        type3Input = "_ruleId"
    elif funName == "addOperationToRule":       
        funHash = (Web3.toHex(text = "rule4") + "0"*64)[:66]

    logs = w3.eth.getLogs({'fromBlock': firstBlock, 'toBlock': lastBlock, 'address': ABACContractAddr, 'topics':[eventNameHash, funHash]}) 
    
    funcRelatedTxs = []
    for log in logs:
        tx = log['transactionHash']    
        funcRelatedTxs.append(tx) 
    funcRelatedTxs.reverse()
  
    for tx in funcRelatedTxs:
        txData = w3.eth.getTransaction(tx)
        inputDataFun, inputData = getInpFunDetails(txData.input)
        isFound = False
        
        if funcType == 1:
            inputSet = set(inputData[type1Input])
            if querySet[type1Query].issubset(inputSet):
                isFound = True
        elif funcType == 2:
            if querySet[type2Query1] == inputData[type2Input]:
                if querySet[type2Query2].issubset(set(inputData['_value'])):
                    isFound = True
        elif funcType == 3:
            if querySet[type3Query1] == inputData[type3Input]:
                attrs = inputData['_attr']
                values = inputData['_value']
                attrValuePair = {}
                for i in range(len(attrs)):
                    attrValuePair[attrs[i]] = values[i]
                if querySet[type3Query2].items() <= attrValuePair.items():
                  isFound = True 
        elif inputDataFun == "addOperationToRule":
            if querySet['ruleId'] == inputData['_ruleId']:
                if querySet['operation'] == inputData['_op']:
                    isFound = True
        
        if isFound:
            txReceipt = w3.eth.getTransactionReceipt(tx)
            resData = {}
            resData['txHash'] = tx.hex()
            resData['inputFunction'] = inputDataFun
            resData['inputData'] = inputData 
            resData['gasUsed'] = txReceipt['gasUsed']
            resData['value'] = txData['value']
            resData['to'] = txReceipt['to']
            resData['from'] = txReceipt['from']
            resTxns.append(resData) 
            txCnt -= 1

            # flash("no of blocks : ", )
        if txCnt == 0:
          break
    return resTxns

### Functions to get Transaction details ####
def getTransactionDetails(txHash):
  TxDetails = w3.eth.getTransaction(txHash)
  TxReceipt = w3.eth.getTransactionReceipt(txHash)
  return TxDetails, TxReceipt


#### Function to insert Access Requests ####
def getAccessibleObjectsBC(userId, operation, objects):
    userIdHex = Web3.toHex(text=userId)
    operationHex = Web3.toHex(text=operation)  
    objectsHex = fStrtoHex(objects)       
    data = ABACContract.encodeABI(fn_name="getAccessibleObjects",args=[userIdHex, operationHex, objectsHex])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash

def checkAccessRequestBC(userId, objectId, operation, accessGiven):
    userIdHex = Web3.toHex(text=userId)
    operationHex = Web3.toHex(text=operation)
    objectIdHex = Web3.toHex(text=objectId)
    data = ABACContract.encodeABI(fn_name="accessRequestPerObject",args=[userIdHex, objectIdHex, operationHex, accessGiven])
    nonce = w3.eth.getTransactionCount(addr1)
    txHash = sendTx(nonce, ABACContractAddr, data)
    return txHash


### Global Variables for multiple request ###
maxNum = 100 #combines 100 transactions before inserting them to blockchain
totNum = 0
start = 1654101572
end = 0
idxArray = []
userIdHex = []
objectIdHex = []
operationHex = []
responseHex = []


nonce = w3.eth.getTransactionCount(addr1)
mutex = Lock()

#### Function to insert multiple access request response ####
def checkMultipleAccessRequestBC(idx, userId, objectId, operation, response):
    mutex.acquire()
    global start, end, maxNum, totNum
    global idxArray, userIdHex, objectIdHex, operationHex, responseHex
    global nonce

    idxArray.append(idx)
    userIdHex.append(Web3.toHex(text=userId))
    objectIdHex.append(Web3.toHex(text=objectId))
    operationHex.append(Web3.toHex(text=operation))
    responseHex.append(response)
    totNum += 1
    start = min(start, idx)
    end = max(end, idx)
    print(totNum)


    if totNum == maxNum :
        data = ABACContract.encodeABI(fn_name="getMultipleResponse",args=[start, end, idxArray, userIdHex, objectIdHex, operationHex, responseHex])
        # nonce = w3.eth.getTransactionCount(addr1)
        txHash = sendTx(nonce, ABACContractAddr, data)
        nonce += 1

        totNum = 0
        start = 1654101572
        end = 0
        idxArray = []
        userIdHex = []
        objectIdHex = []
        operationHex = []
        responseHex = []

    mutex.release()