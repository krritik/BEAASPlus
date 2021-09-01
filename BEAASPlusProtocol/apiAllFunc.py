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
    global ABACOpt5rawJSON, ABACOpt5ABI, ABACOpt5Contract, ABACContract
    ABACOpt5rawJSON = _abi
    ABACOpt5ABI = json.loads(ABACOpt5rawJSON)
    ABACOpt5Contract = w3.eth.contract(address=ABACOpt5Addr, abi=ABACOpt5ABI)
    ABACContract = ABACOpt5Contract


#### Update ABAC components
def fHexbyteToStr(_arr):
    if isinstance(_arr, list):
      res = [ x.decode('utf8').rstrip('\x00') for x in _arr]
    else:
      res = _arr.decode('utf8').rstrip('\x00')
    return res

def getInpFunDetails(_input):
    decodedInput = ABACContract.decode_function_input(_input)
    funName = str(decodedInput[0]).split()[1].split('(')[0]
    funAttr = decodedInput[1]
    for x in funAttr:
      funAttr[x] = fHexbyteToStr(funAttr[x])
    return funName, funAttr

def createEventFilterUpdateABAC(_funcName, _lastBlock, _latestBlock='latest'):
    eventNameHash = w3.keccak(
            text="functionAccessed(bytes32)").hex()
    funHash = (Web3.toHex(text = _funcName) + "0"*64)[:66]

    eventFilter = w3.eth.filter({
        "address": ABACContractAddr,
        "topics": [eventNameHash, funHash],
        "fromBlock": _lastBlock,
        "toBlock": _latestBlock
    })
    return eventFilter

def verifyABACUpdate(_queryData, _funcName, _trueCallback, _tArgs, _falseCallback, _fArgs):
    lastBlock = w3.eth.blockNumber
    latestEvent = "NULL"
    eventFilter = createEventFilterUpdateABAC(_funcName, lastBlock)

    prevEvents = eventFilter.get_all_entries()
    if prevEvents:
        latestEvent = prevEvents[-1]

    if latestEvent == "NULL":
        while True:
            events = eventFilter.get_new_entries()
            if events:
                latestEvent = events[-1]
                break
            time.sleep(0.1)

    tx = latestEvent['transactionHash']
    txData = w3.eth.getTransaction(tx)
    inputDataFun, inputData = getInpFunDetails(txData.input)

    res = False

    if _funcName == "user1" and set(_queryData) == set(inputData["_U"]):
        res = True
    elif _funcName == "user2" and set(_queryData) == set(inputData["_UA"]):
        res = True
    elif _funcName == "user3":
        attr = list(_queryData.keys())[0]
        if attr == inputData["_UA"]:
            if _queryData[attr] == inputData["_value"]:
                res = True
    elif _funcName == "user4":
        qd2 = _queryData.copy()
        userId = qd2.pop("userId")
        if userId == inputData["_U"]:
            attrs = inputData['_attr']
            values = inputData['_value']
            attrValuePair = {}
            for i in range(len(attrs)):
                attrValuePair[attrs[i]] = values[i]
    
            if attrValuePair == qd2:
                res = True
    
    elif _funcName == "object1" and set(_queryData) == set(inputData["_O"]):
        res = True
    elif _funcName == "object2" and set(_queryData) == set(inputData["_OA"]):
        res = True
    elif _funcName == "object3":
        attr = list(_queryData.keys())[0]
        if attr == inputData["_OA"]:
            if _queryData[attr] == inputData["_value"]:
                res = True
    elif _funcName == "object4":
        qd2 = _queryData.copy()
        objectId = qd2.pop("objectId")
        if objectId == inputData["_O"]:
            attrs = inputData['_attr']
            values = inputData['_value']
            attrValuePair = {}
            for i in range(len(attrs)):
                attrValuePair[attrs[i]] = values[i]
        
            if attrValuePair == qd2:
                res = True

    elif _funcName == "operation" and set(_queryData) == set(inputData["_OP"]):
        res = True
    elif _funcName == "rule1" and set(_queryData) == set(inputData["_rules"]):
        res = True

    elif _funcName == "rule2" or _funcName == "rule3":
        qd2 = _queryData.copy()
        ruleId = qd2.pop("ruleId")
        if ruleId == inputData["_ruleId"]:
            attrs = inputData['_attr']
            values = inputData['_val']
            attrValuePair = {}
            for i in range(len(attrs)):
                attrValuePair[attrs[i]] = values[i]
    
            if attrValuePair == qd2:
                res = True
    elif _funcName == "rule4" and _queryData["ruleId"] == inputData["_ruleId"] and _queryData["operation"] == inputData["_op"]:
        res = True
    print("")
    if res == False:
        if _trueCallback != None:
            _trueCallback(*_tArgs)
        print("ERROR : result in blockchain differs")
    else:
        if _falseCallback != None:
            _falseCallback(*_fArgs) 
        print("OK : data added correctly in blockchain : \n txHash -> " + str(tx))
    print(_queryData)
    print(inputData)
    print("")
    return



def addUsers(_users, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_users)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return
    
    data = {}
    for i in range(len1):
        data["user"+str(i+1)] = _users[i]
    url = appURL + '/createUsers'
    req = requests.post(url, data=data)  

    if req.status_code == 200:
        print("\nadd users done")
        print(_users)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_users,"user1", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addUserAttributes(_userAttributes, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_userAttributes)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return
    
    data = {}
    for i in range(len1) :
        data["attr"+str(i+1)] = _userAttributes[i]
    url = appURL + '/createUserAttributes'
    req = requests.post(url, data=data)    
    
    if req.status_code == 200:
        print("\nadd user attributes done")
        print(_userAttributes)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_userAttributes,"user2", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addUserAttributePosValues(_userAttribute, _attributeValues, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_attributeValues)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return
    
    data = {"attr" : _userAttribute}
    for i in range(len1):
        data["value"+str(i+1)] = _attributeValues[i]
    url = appURL + '/createUserAttributePosValues'
    req = requests.post(url, data=data)    
    
    _UAP = { _userAttribute : _attributeValues }

    if req.status_code == 200:
        print("\nadd user attribute values done")
        print(_UAP)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_UAP,"user3", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addUserAttributeValuePair(_userId, _attributes, _values, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    data = { "userId" : _userId}
    for i in range(len(_attributes)):
        data[_attributes[i]] = _values[i] 
    url = appURL + '/createUserAttributeValuePair'
    req = requests.post(url, data=data)    

    if req.status_code == 200:
        print("\nadd user attribute values done")
        print(data)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(data,"user4", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("Error request failed with status code : " + str(req.status_code)) 

def addObjects(_objects, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_objects)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return
    
    data = {}
    for i in range(len1):
        data["object"+str(i+1)] = _objects[i]
    url = appURL + '/createObjects'
    req = requests.post(url, data=data)  

    if req.status_code == 200:
        print("add objects done")
        print(_objects)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_objects,"object1", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("Error request failed with status code : " + str(req.status_code))

def addObjectAttributes(_objectAttributes, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_objectAttributes)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return

    data = {}
    for i in range(len1) :
        data["attr"+str(i+1)] = _objectAttributes[i]
    url = appURL + '/createObjectAttributes'
    req = requests.post(url, data=data)    
    
    if req.status_code == 200:
        print("\nadd object attributes done")
        print(_objectAttributes)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_objectAttributes,"object2", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addObjectAttributePosValues(_objectAttribute, _attributeValues, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_attributeValues)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return
    
    data = {"attr" : _objectAttribute}
    for i in range(len(_attributeValues)):
        data["value"+str(i+1)] = _attributeValues[i]
    url = appURL + '/createObjectAttributePosValues'
    req = requests.post(url, data=data)    
    
    _OAP = { _objectAttribute : _attributeValues }

    if req.status_code == 200:
        print("\nadd object attribute values done")
        print(_OAP)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_OAP,"object3", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addObjectAttributeValuePair(_objectId, _attributes, _values, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    data = { "objectId" : _objectId}
    for i in range(len(_attributes)):
        data[_attributes[i]] = _values[i] 
    url = appURL + '/createObjectAttributeValuePair'
    req = requests.post(url, data=data)    

    if req.status_code == 200:
        print("\nadd object attribute values done")
        print(data)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(data,"object4", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code)) 

def addOperations(_operations, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_operations)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return

    data = {}
    for i in range(len1):
        data["operation"+str(i+1)] = _operations[i]
    url = appURL + '/createOperations'
    req = requests.post(url, data=data)  

    if req.status_code == 200:
        print("\nadd operations done")
        print(_operations)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_operations,"operation", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addRules(_rules, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    len1 = len(_rules)
    if len1 > 4:
        print("ERROR: no of elements should be less than 5")
        return

    data = {}
    for i in range(len1):
        data["rule"+str(i+1)] = _rules[i]
    url = appURL + '/createRules'
    req = requests.post(url, data=data)  

    if req.status_code == 200:
        print("\nadd rules done")
        print(_rules)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(_rules,"rule1", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("Error request failed with status code : " + str(req.status_code))


def addOperationToRule(_ruleId, _operation, _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    data = {
        'ruleId' : _ruleId,
        'operation': _operation
    }

    url = appURL + '/createRuleAttributeValuePair'
    req = requests.post(url, data=data)  

    if req.status_code == 200:
        print("\nadd operation to rules done")
        print(data)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(data,"rule4", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))


def addUserToRule(_ruleId, _attributes, _values , _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    data = { "ruleId" : _ruleId}
    for i in range(len(_attributes)):
        data[_attributes[i]] = _values[i] 
    url = appURL + '/createRuleAttributeValuePair'
    req = requests.post(url, data=data)    

    if req.status_code == 200:
        print("\nadd user attribute value pair to rule done")
        print(data)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(data,"rule2", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))

def addObjectToRule(_ruleId, _attributes, _values , _trueCallback=None, _tArgs=(), _falseCallback=None, _fArgs=()):
    data = { "ruleId" : _ruleId}
    for i in range(len(_attributes)):
        data[_attributes[i]] = _values[i] 
    url = appURL + '/createRuleAttributeValuePair'
    req = requests.post(url, data=data)    

    if req.status_code == 200:
        print("\nadd object attribute value pair to rule done")
        print(data)
        print("")
        t1 = threading.Thread(target=verifyABACUpdate, args=(data,"rule3", _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return
    else:
        print("\nError request failed with status code : " + str(req.status_code))



#### Check Access Request
def createEventFilterAccessRequest(_userId, _objectId, _operation, _lastBlock, _latestBlock='latest'):
    eventNameHash = w3.keccak(
        text="accessRequestResponse(bytes32,bytes32,bytes32,bool)").hex()
    userIdHash = (Web3.toHex(text=_userId) + "0"*64)[:66]
    objectIdHash = (Web3.toHex(text=_objectId) + "0"*64)[:66]
    operationHash = (Web3.toHex(text=_operation) + "0"*64)[:66]

    eventFilter = w3.eth.filter({
        "address": ABACContractAddr,
        "topics": [eventNameHash, userIdHash, objectIdHash, operationHash],
        "fromBlock": _lastBlock,
        "toBlock": _latestBlock
    })
    return eventFilter

def verifyAccessRequest(_data, _expectedRes, _trueCallback, _tArgs, _falseCallback, _fArgs):
    lastBlock = max(0, w3.eth.blockNumber-200)
    latestEvent = "NULL"
    trueRes = "false"
    isMatched = False

    eventFilter = createEventFilterAccessRequest(_data['userId'], _data['objectId'], _data['operation'], lastBlock)
    prevEvents = eventFilter.get_all_entries()

    if prevEvents:
        latestEvent = prevEvents[-1]
        if int(latestEvent['data'][-1]) == 1:
            trueRes = "true"

        if trueRes == _expectedRes:
            isMatched = True
    
    if latestEvent == "NULL":
        while True:
            events = eventFilter.get_new_entries()
            if events:
                latestEvent = events[-1]
                if int(latestEvent['data'][-1]) == 1:
                    trueRes = "true"

                if trueRes == _expectedRes:
                    isMatched = True
                return
            time.sleep(0.1)    

    if isMatched:
        if _trueCallback != None:
            _trueCallback(*_tArgs)
        print("ERROR : result in blockchain differs")
        print("")
    else :
        if _falseCallback != None:
            _falseCallback(*_fArgs)
        print("OK : response added correctly in blockchain : \n txHash -> " + str(latestEvent['transactionHash']))
        print("")
    return

def checkAccessRequest(_userId, _objectId, _operation, _trueCallback = None, _tArgs = (), _falseCallback = None, _fArgs = ()):
    url = appURL + '/getAccessRequest'

    data = {
        'userId': _userId,
        'operation': _operation,
        'objectId': _objectId
    }
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    returnedRes = requests.get(url, data=data_json, headers=headers)

    if returnedRes.status_code == 200:
        res = str(returnedRes.text)[:-1]
        print("response from server : " + str(res))
        print("")
        t1 = threading.Thread(target=verifyAccessRequest, args=(data,res, _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return res
    else:
        print('status code :' + str(returnedRes.status_code))



### Check multiple access request
def createEventFilterMultipleRequest(_lastBlock=0, _latestBlock='latest'):
    eventNameHash = w3.keccak(
        text="accessMultipleResponse(uint256,uint256,uint256[],bytes32[],bytes32[],bytes32[],bool[])").hex()

    eventFilter = w3.eth.filter({
        "address": ABACContractAddr,
        "topics": [eventNameHash],
        "fromBlock": _lastBlock,
        "toBlock": _latestBlock
    })
    return eventFilter

def verifyMultipleAccessRequest(_data, _trueCallback, _tArgs, _falseCallback, _fArgs):
    lastBlock = max(0, w3.eth.blockNumber-200)
    resMatched = False
    isFound = False

    eventFilter = createEventFilterMultipleRequest(lastBlock)
    prevEvents = eventFilter.get_all_entries()

    if prevEvents:
        for latestEvent in prevEvents:
            txHash = latestEvent['transactionHash']
            receipt = w3.eth.getTransactionReceipt(txHash)
            log = ABACContract.events.accessMultipleResponse().processReceipt(receipt)
            logArgs = log[0]['args']
            
            if _data['idx'] >= logArgs['start'] and _data['idx'] <= logArgs['end']:
                isFound = True
                break

    if isFound == False:
        while True:
            events = eventFilter.get_new_entries()
            if events:
                for latestEvent in prevEvents:
                    latestEvent = events[-1]
                    txHash = latestEvent['transactionHash']
                    receipt = w3.eth.getTransactionReceipt(txHash)
                    log = ABACContract.events.accessMultipleResponse().processReceipt(receipt)
                    logArgs = log[0]['args']
        
                    if _data['idx'] >= logArgs['start'] and _data['idx'] <= logArgs['end']:
                        isFound = True
                        break
                if isFound:
                    break
            time.sleep(0.1)

    idxArray = logArgs['idx']
    idx = idxArray.index(_data['idx'])
    if logArgs['userId'][idx] == _data['userId'] and logArgs['objectId'][idx] == _data['objectId']:
        if logArgs['operation'][idx] == _data['operation'] and logArgs['response'][idx] == _data['operation']:
            resMatched = True

    if resMatched:
        if _trueCallback != None:
            _trueCallback(*_tArgs) 
        print("ERROR : result in blockchain differs")
    else :
        if _falseCallback != None:
            _falseCallback(*_fArgs)
        print("OK : response added correctly in blockchain : \n txHash -> " + str(latestEvent['transactionHash']))
        print("response in blockchain : " + str(_data['response'])) 
        print("")
    return
    

def checkMultipleAccessRequest(_userId, _objectId, _operation, _trueCallback = None, _tArgs = (), _falseCallback = None, _fArgs = ()):
    url = appURL + '/getMultipleAccessRequest'

    data = {
        'idx': int(time.time()),
        'userId': _userId,
        'operation': _operation,
        'objectId': _objectId
    }
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    returnedRes = requests.get(url, data=data_json, headers=headers)

    if returnedRes.status_code == 200:
        res = str(returnedRes.text)[:-1]
        data['response'] = res
        print("response from server : " + str(res))
        print("")
        t1 = threading.Thread(target=verifyMultipleAccessRequest, args=(data, _trueCallback, _tArgs, _falseCallback, _fArgs))
        t1.start()
        return res
    else:
        print('status code :' + str(returnedRes.status_code))