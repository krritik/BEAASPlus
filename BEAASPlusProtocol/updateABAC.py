# from base import *

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