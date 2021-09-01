# from base import *

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