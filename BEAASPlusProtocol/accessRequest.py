# from base import *

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