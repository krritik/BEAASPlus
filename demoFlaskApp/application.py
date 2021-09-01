from flask import Flask, flash, request, url_for, redirect, render_template, jsonify
from ABACdb import * 
from ABACblockchain import *
from datetime import date
import time
import datetime
import threading

application = Flask(__name__)
application.secret_key = "super secret key"
application.config["TEMPLATES_AUTO_RELOAD"] = True

@application.route('/')
def hello():
    flash('Welcome to Home Page')
    initialDatabase()
    return render_template('home.html')

#### Functions for Users
@application.route('/createUsers', methods=['GET', 'POST'])
def createUsers():
    start = datetime.datetime.now()
    if request.method == 'POST':
        users = []
        
        if 'user1' in request.form and request.form['user1']:
            users.append(request.form['user1'])
        if 'user2' in request.form and request.form['user2']:
            users.append(request.form['user2'])
        if 'user3' in request.form and request.form['user3']:
            users.append(request.form['user3'])
        if 'user4' in request.form and request.form['user4']:
            users.append(request.form['user4'])
        insertUsersDB(users)
        end = datetime.datetime.now()
        timeDiff = end-start
        # print(timeDiff.total_seconds()*1000)
        # flash("Updation Time for users : " + str(timeDiff.total_seconds()*1000))
        return render_template('done.html')
    else:
        return render_template('createUsers.html') 

@application.route('/createUserAttributes', methods=['GET', 'POST'])
def createUserAttributes():
    start = datetime.datetime.now()
    if request.method == 'POST':
        attrs = []
        
        if 'attr1' in request.form and request.form['attr1']:
            attrs.append(request.form['attr1'])
        if 'attr2' in request.form and request.form['attr2']:
            attrs.append(request.form['attr2'])
        if 'attr3' in request.form and request.form['attr3']:
            attrs.append(request.form['attr3'])
        if 'attr4' in request.form and request.form['attr4']:
            attrs.append(request.form['attr4'])
        
        insertUserAttributesDB(attrs)
        end = datetime.datetime.now()
        timeDiff = end-start
        # print(timeDiff.total_seconds()*1000)
        # flash("Updation Time for users : " + str(timeDiff.total_seconds()*1000))
        return render_template('done.html')
    else:
        return render_template('createUserAttributes.html')         


@application.route('/createUserAttributePosValues', methods=['GET', 'POST'])
def createUserAttrValues():
    start = datetime.datetime.now()
    if request.method == 'POST':
        attr = ""
        values = []
        
        if request.form['attr']:
            attr = request.form['attr']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error)

        if 'value1' in request.form and request.form['value1']:
            values.append(request.form['value1'])
        if 'value2' in request.form and request.form['value2']:
            values.append(request.form['value2'])
        if 'value3' in request.form and request.form['value3']:
            values.append(request.form['value3'])
        if 'value4' in request.form and request.form['value4']:
            values.append(request.form['value4'])
       
        insertUserAttributePosValuesDB(attr, values)
        end = datetime.datetime.now()
        timeDiff = end-start
        # print(timeDiff.total_seconds()*1000)
        # flash("Updation Time for users : " + str(timeDiff.total_seconds()*1000))
        return render_template('done.html')
    else:
        userAttrs = getUserAttributesDB()
        return render_template('createUserAttributePosValues.html', userAttrs=userAttrs)  

@application.route('/createUserAttributeValuePair', methods=['GET', 'POST'])
def createUserAttributeValuePair():
    start = datetime.datetime.now()
    userAttrs = getUserAttributesDB()

    if request.method == 'POST':
        userId = ""
        attrValuePair = {}

        if request.form['userId']:
            userId = request.form['userId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        for attr in userAttrs:
            if attr in request.form and request.form[attr]:
                attrValuePair[attr] = request.form[attr]
        insertUserAttributeValuePairDB(userId, attrValuePair)
       
        end = datetime.datetime.now()
        timeDiff = end-start
        # print(timeDiff.total_seconds()*1000)
        # flash("Updation Time for users : " + str(timeDiff.total_seconds()*1000))
        return render_template('done.html')
    else:
        users = getUsersDB()
        attrValueOptions = {} 
        for attr in userAttrs:
            attrValueOptions[attr] = getUserAttributePosValuesDB(attr)
        return render_template('createUserAttributeValuePair.html', users = users, attrValueOptions=attrValueOptions)  


###### Functions for Objects
@application.route('/createObjects', methods=['GET', 'POST'])
def createObjects():
    if request.method == 'POST':
        objects = []
        
        if 'object1' in request.form and request.form['object1']:
            objects.append(request.form['object1'])
        if 'object2' in request.form and request.form['object2']:
            objects.append(request.form['object2'])
        if 'object3' in request.form and request.form['object3']:
            objects.append(request.form['object3'])
        if 'object4' in request.form and request.form['object4']:
            objects.append(request.form['object4'])
        
        insertObjectsDB(objects)
        return render_template('done.html')
    else:
        return render_template('createObjects.html') 

@application.route('/createObjectAttributes', methods=['GET', 'POST'])
def createObjectAttributes():
    if request.method == 'POST':
        attrs = []
        
        if 'attr1' in request.form and request.form['attr1']:
            attrs.append(request.form['attr1'])
        if 'attr2' in request.form and request.form['attr2']:
            attrs.append(request.form['attr2'])
        if 'attr3' in request.form and request.form['attr3']:
            attrs.append(request.form['attr3'])
        if 'attr4' in request.form and request.form['attr4']:
            attrs.append(request.form['attr4'])
        
        insertObjectAttributesDB(attrs)
        return render_template('done.html')
    else:
        return render_template('createObjectAttributes.html')         


@application.route('/createObjectAttributePosValues', methods=['GET', 'POST'])
def createObjectAttrValues():
    if request.method == 'POST':
        attr = ""
        values = []
        
        if request.form['attr']:
            attr = request.form['attr']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error)

        if 'value1' in request.form and request.form['value1']:
            values.append(request.form['value1'])
        if 'value2' in request.form and request.form['value2']:
            values.append(request.form['value2'])
        if 'value3' in request.form and request.form['value3']:
            values.append(request.form['value3'])
        if 'value4' in request.form and request.form['value4']:
            values.append(request.form['value4'])
       
        insertObjectAttributePosValuesDB(attr, values)
        return render_template('done.html')
    else:
        objectAttrs = getObjectAttributesDB()
        return render_template('createObjectAttributePosValues.html', objectAttrs=objectAttrs)  

@application.route('/createObjectAttributeValuePair', methods=['GET', 'POST'])
def createObjectAttributeValuePair():
    objectAttrs = getObjectAttributesDB()

    if request.method == 'POST':
        objectId = ""
        attrValuePair = {}

        if request.form['objectId']:
            objectId = request.form['objectId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        for attr in objectAttrs:
            if attr in request.form and request.form[attr]:
                attrValuePair[attr] = request.form[attr]
        insertObjectAttributeValuePairDB(objectId, attrValuePair)
        return render_template('done.html')
    else:
        objects = getObjectsDB()
        attrValueOptions = {} 
        for attr in objectAttrs:
            attrValueOptions[attr] = getObjectAttributePosValuesDB(attr)
        return render_template('createObjectAttributeValuePair.html', objects = objects, attrValueOptions=attrValueOptions)



@application.route('/createOperations', methods=['GET', 'POST'])
def createOperations():
    if request.method == 'POST':
        operations = []
        
        if 'operation1' in request.form and request.form['operation1']:
            operations.append(request.form['operation1'])
        if 'operation2' in request.form and request.form['operation2']:
            operations.append(request.form['operation2'])
        if 'operation3' in request.form and request.form['operation3']:
            operations.append(request.form['operation3'])
        if 'operation4' in request.form and request.form['operation4']:
            operations.append(request.form['operation4'])
        
        insertOperationsDB(operations)
        return render_template('done.html')
    else:
        return render_template('createOperations.html') 


##### For Rules

@application.route('/createRules', methods=['GET', 'POST'])
def createRules():
    if request.method == 'POST':
        rules = []
        
        if 'rule1' in request.form and request.form['rule1']:
            rules.append(request.form['rule1'])
        if 'rule2' in request.form and request.form['rule2']:
            rules.append(request.form['rule2'])
        if 'rule3' in request.form and request.form['rule3']:
            rules.append(request.form['rule3'])
        if 'rule4' in request.form and request.form['rule4']:
            rules.append(request.form['rule4'])
        
        insertRulesDB(rules)
        return render_template('done.html')
    else:
        return render_template('createRules.html')   

@application.route('/createRuleAttributeValuePair', methods=['GET', 'POSt']) 
def createRuleAttributeValuePair():
    userAttrs = getUserAttributesDB()
    objectAttrs = getObjectAttributesDB()

    if request.method == 'POST':
        ruleId = ""
        operation = ""
        userAttrValuePair = {}  
        objectAttrValuePair = {}

        if request.form['ruleId']:
            ruleId = request.form['ruleId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 
        if "operation" in request.form and request.form['operation']:
            operation = request.form['operation']
            insertRuleOperationDB(ruleId, operation)

        for attr in userAttrs:
            if attr in request.form and request.form[attr]:
                userAttrValuePair[attr] = request.form[attr] 
        for attr in objectAttrs:
            if attr in request.form and request.form[attr]:
                objectAttrValuePair[attr] = request.form[attr]
        if userAttrValuePair:
            time.sleep(20)
            insertRuleUserDB(ruleId, userAttrValuePair)
        if objectAttrValuePair:
            time.sleep(20)
            insertRuleObjectDB(ruleId, objectAttrValuePair)
        return render_template('done.html')
    else:
        rules = getRulesDB()
        operations = getOperationsDB()
        userAttrValueOptions = {} 
        objectAttrValueOptions = {}
        for attr in userAttrs:
            userAttrValueOptions[attr] = getUserAttributePosValuesDB(attr)
        for attr in objectAttrs:
            objectAttrValueOptions[attr] = getObjectAttributePosValuesDB(attr)    
        return render_template('/createRuleAttributeValuePair.html',rules=rules,operations=operations,userAttrValueOptions=userAttrValueOptions,objectAttrValueOptions=objectAttrValueOptions)


########################## Verify transactions in blockchain ###########
@application.route('/verifyUsers', methods=["GET", "POST"])
def verifyUsers():
    start = datetime.datetime.now()
    if request.method == 'POST':
        users = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['user1']:
            users.append(request.form['user1'])
        if request.form['user2']:
            users.append(request.form['user2'])
        if request.form['user3']:
            users.append(request.form['user3'])
        if request.form['user4']:
            users.append(request.form['user4'])
        querySet =  {}
        querySet["users"] = set(users)
        txns = verifyTransactions("addUsers", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addUsers", querySet, txCnt, noOfBlocks, timeStamp)

        end = datetime.datetime.now()
        timeDiff = end-start
        # print("Verification Time for users : ", timeDiff.total_seconds()*1000)
        # flash("Verification Time for users : " + str(timeDiff.total_seconds()*1000))
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyUsers.html')

@application.route('/verifyUserAttributes', methods=["GET", "POST"])
def verifyUserAttributes():
    if request.method == 'POST':
        attrs = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['attr1']:
            attrs.append(request.form['attr1'])
        if request.form['attr2']:
            attrs.append(request.form['attr2'])
        if request.form['attr3']:
            attrs.append(request.form['attr3'])
        if request.form['attr4']:
            attrs.append(request.form['attr4'])

        querySet =  {}
        querySet["userAttributes"] = set(attrs)
        txns = verifyTransactions("addUserAttributes", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addUserAttributes", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyUserAttributes.html')   

@application.route('/verifyUserAttributePosValues', methods=["GET", "POST"])
def verifyUserAttributePosValues():
    if request.method == 'POST':
        attr = ""
        values = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['attr']:
            attr = request.form['attr']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error)
        if request.form['value1']:
            values.append(request.form['value1'])
        if request.form['value2']:
            values.append(request.form['value2'])
        if request.form['value3']:
            values.append(request.form['value3'])
        if request.form['value4']:
            values.append(request.form['value4'])
       
        querySet =  {}
        querySet["userAttributeName"] = attr
        querySet["userAttributeValues"] = set(values)
        txns = verifyTransactions("addUserAttributePosValues", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addUserAttributePosValues", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyUserAttributePosValues.html')

@application.route('/verifyUserAttributeValuePair', methods=["GET", "POST"])
def verifyUserAttributeValuePair():
    if request.method == 'POST':
        userId = ""
        attrValuePair = {}

        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['userId']:
            userId = request.form['userId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        if request.form['attr1']:
            attr1 = request.form['attr1']
            attrValuePair[attr1] = request.form['value1']
        if request.form['attr2']:
            attr2 = request.form['attr2']
            attrValuePair[attr2] = request.form['value2']
        if request.form['attr3']:
            attr3 = request.form['attr3']
            attrValuePair[attr3] = request.form['value3']
        if request.form['attr4']:
            attr4 = request.form['attr4']
            attrValuePair[attr4] = request.form['value4']
        if request.form['attr5']:
            attr5 = request.form['attr5']
            attrValuePair[attr5] = request.form['value5']
    
        querySet = {}
        querySet['userId'] = userId
        querySet['userAttributeValuePair'] = attrValuePair
        txns = verifyTransactions("addUserAttributeValuePair", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addUserAttributeValuePair", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyUserAttributeValuePair.html')      


@application.route('/verifyObjects', methods=["GET", "POST"])
def verifyObjects():
    if request.method == 'POST':
        objects = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['object1']:
            objects.append(request.form['object1'])
        if request.form['object2']:
            objects.append(request.form['object2'])
        if request.form['object3']:
            objects.append(request.form['object3'])
        if request.form['object4']:
            objects.append(request.form['object4'])

        querySet =  {}
        querySet["objects"] = set(objects)
        txns = verifyTransactions("addObjects", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addObjects", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyObjects.html')

@application.route('/verifyObjectAttributes', methods=["GET", "POST"])
def verifyObjectAttributes():
    if request.method == 'POST':
        attrs = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['attr1']:
            attrs.append(request.form['attr1'])
        if request.form['attr2']:
            attrs.append(request.form['attr2'])
        if request.form['attr3']:
            attrs.append(request.form['attr3'])
        if request.form['attr4']:
            attrs.append(request.form['attr4'])

        querySet =  {}
        querySet["objectAttributes"] = set(attrs)
        txns = verifyTransactions("addObjectAttributes", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addObjectAttributes", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyObjectAttributes.html')   

@application.route('/verifyObjectAttributePosValues', methods=["GET", "POST"])
def verifyObjectAttributePosValues():
    if request.method == 'POST':
        attr = ""
        values = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['attr']:
            attr = request.form['attr']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error)
        if request.form['value1']:
            values.append(request.form['value1'])
        if request.form['value2']:
            values.append(request.form['value2'])
        if request.form['value3']:
            values.append(request.form['value3'])
        if request.form['value4']:
            values.append(request.form['value4'])
       
        querySet =  {}
        querySet["objectAttributeName"] = attr
        querySet["objectAttributeValues"] = set(values)
        txns = verifyTransactions("addObjectAttributePosValues", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addObjectAttributePosValues", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyObjectAttributePosValues.html')

@application.route('/verifyObjectAttributeValuePair', methods=["GET", "POST"])
def verifyObjectAttributeValuePair():
    if request.method == 'POST':
        objectId = ""
        attrValuePair = {}
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['objectId']:
            objectId = request.form['objectId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        if request.form['attr1']:
            attr1 = request.form['attr1']
            attrValuePair[attr1] = request.form['value1']
        if request.form['attr2']:
            attr2 = request.form['attr2']
            attrValuePair[attr2] = request.form['value2']
        if request.form['attr3']:
            attr3 = request.form['attr3']
            attrValuePair[attr3] = request.form['value3']
        if request.form['attr4']:
            attr4 = request.form['attr4']
            attrValuePair[attr4] = request.form['value4']
        if request.form['attr5']:
            attr5 = request.form['attr5']
            attrValuePair[attr5] = request.form['value5']
    
        querySet = {}
        querySet['objectId'] = objectId
        querySet['objectAttributeValuePair'] = attrValuePair
        txns = verifyTransactions("addObjectAttributeValuePair", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addObjectAttributeValuePair", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyObjectAttributeValuePair.html')   


@application.route('/verifyOperations', methods=["GET", "POST"])
def verifyOperations():
    if request.method == 'POST':
        operations = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])


        if request.form['operation1']:
            operations.append(request.form['operation1'])
        if request.form['operation2']:
            operations.append(request.form['operation2'])
        if request.form['operation3']:
            operations.append(request.form['operation3'])
        if request.form['operation4']:
            operations.append(request.form['operation4'])

        querySet =  {}
        querySet["operations"] = set(operations)
        txns = verifyTransactions("addOperations", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addOperations", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyOperations.html')


@application.route('/verifyRules', methods=["GET", "POST"])
def verifyRules():
    if request.method == 'POST':
        rules = []
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])
        
        if request.form['rule1']:
            rules.append(request.form['rule1'])
        if request.form['rule2']:
            rules.append(request.form['rule2'])
        if request.form['rule3']:
            rules.append(request.form['rule3'])
        if request.form['rule4']:
            rules.append(request.form['rule4'])

        querySet =  {}
        querySet["rules"] = set(rules)
        txns = verifyTransactions("addRules", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addRules", querySet, txCnt, noOfBlocks,  timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyRules.html')

@application.route('/verifyRuleUser', methods=["GET", "POST"])
def verifyRuleUser():
    if request.method == 'POST':
        ruleId = ""
        attrValuePair = {}
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['ruleId']:
            ruleId = request.form['ruleId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        if request.form['attr1']:
            attr1 = request.form['attr1']
            attrValuePair[attr1] = request.form['value1']
        if request.form['attr2']:
            attr2 = request.form['attr2']
            attrValuePair[attr2] = request.form['value2']
        if request.form['attr3']:
            attr3 = request.form['attr3']
            attrValuePair[attr3] = request.form['value3']
        if request.form['attr4']:
            attr4 = request.form['attr4']
            attrValuePair[attr4] = request.form['value4']
        if request.form['attr5']:
            attr5 = request.form['attr5']
            attrValuePair[attr5] = request.form['value5']
    
        querySet = {}
        querySet['ruleId'] = ruleId
        querySet['userAttributeValuePair'] = attrValuePair
        txns = verifyTransactions("addUserAttributeValuePairToRule", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addUserAttributeValuePairToRule", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyRuleUser.html')

@application.route('/verifyRuleObject', methods=["GET", "POST"])
def verifyRuleObject():
    if request.method == 'POST':
        ruleId = ""
        attrValuePair = {}
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['ruleId']:
            ruleId = request.form['ruleId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        if request.form['attr1']:
            attr1 = request.form['attr1']
            attrValuePair[attr1] = request.form['value1']
        if request.form['attr2']:
            attr2 = request.form['attr2']
            attrValuePair[attr2] = request.form['value2']
        if request.form['attr3']:
            attr3 = request.form['attr3']
            attrValuePair[attr3] = request.form['value3']
        if request.form['attr4']:
            attr4 = request.form['attr4']
            attrValuePair[attr4] = request.form['value4']
        if request.form['attr5']:
            attr5 = request.form['attr5']
            attrValuePair[attr5] = request.form['value5']
    
        querySet = {}
        querySet['ruleId'] = ruleId
        querySet['objectAttributeValuePair'] = attrValuePair
        txns = verifyTransactions("addObjectAttributeValuePairToRule", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addObjectAttributeValuePairToRule", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyRuleObject.html')

@application.route('/verifyRuleOperation', methods=["GET", "POST"])
def verifyRuleOperation():
    if request.method == 'POST':
        ruleId = ""
        operation = ""
        # timeStamp = "0"
        noOfBlocks = -1
        txCnt = 1
        
        # if request.form['date']:
        #     timeStamp = request.form['date']
        #     timeStamp = date.fromisoformat(timeStamp).strftime('%s')
        if request.form['txCnt']:
            txCnt = int(request.form['txCnt'])
        if request.form['noOfBlocks']:
            noOfBlocks = int(request.form['noOfBlocks'])

        if request.form['ruleId']:
            ruleId = request.form['ruleId']
        else:
            error = "missing atrribute value"
            render_template('error.html', error=error) 

        if request.form['operation']:
            operation = request.form['operation']
            
        querySet = {}
        querySet['ruleId'] = ruleId
        querySet['operation'] = operation
        txns = verifyTransactions("addOperationToRule", querySet, txCnt, noOfBlocks)
        # txns = verifyTransactions("addOperationToRule", querySet, txCnt, noOfBlocks, timeStamp)
        return render_template('showTxDetails.html', txns= txns)    
    else:
        return render_template('verifyRuleOperation.html')

@application.route('/showUniqueTx/<txHash>', methods=["GET"])
def showUniqueTx(txHash):
    txDetails, txReceipt = getTransactionDetails(txHash)
    return render_template('showUniqueTx.html',txHash=txHash, txDetails = txDetails, txReceipt=txReceipt)


@application.route('/getAccessibleObjectRequest', methods=["GET"])
def getAccessibleObjectRequest():
    postedData = request.get_json()
    userId = postedData['userId']
    operation = postedData['operation']
    objects = findAccessibleObjects(userId, operation)
    getAccessibleObjectsBC(userId, operation, objects)
    return jsonify(objects)

@application.route('/getAccessRequest', methods=["GET"])
def getAccessRequest():
    postedData = request.get_json()
    userId = postedData['userId']
    operation = postedData['operation']
    objectId = postedData['objectId']
    res = checkAccessRequest(userId, objectId, operation)
    # checkAccessRequestBC(userId, objectId, operation, res)
    t1 = threading.Thread(target=checkAccessRequestBC, args=(userId, objectId, operation, res))
    t1.start()
    return jsonify(res)

@application.route('/getMultipleAccessRequest', methods=["GET"])
def getMultipleAccessRequest():
    postedData = request.get_json()
    idx = postedData['idx']    
    userId = postedData['userId']
    operation = postedData['operation']
    objectId = postedData['objectId']
    res = checkAccessRequest(userId, objectId, operation)
    
    # checkMultipleAccessRequestBC(idx, userId, objectId, operation, res)
    t1 = threading.Thread(target=checkMultipleAccessRequestBC, args=(idx, userId, objectId, operation, res))
    t1.start()
    return jsonify(res)

def findAccessibleObjects(userId, operation):
    objects = getObjectsDB()
    accessibleObjects = []

    for obj in objects:
        res = checkAccessRequest(userId, obj, operation)
        if res == True:
            accessibleObjects.append(obj)
    return accessibleObjects

def checkAccessRequest(userId, objectId, operation):
    rules = getRulesDB()
    userAttributeValuePair = getUserAttributeValuePairDB(userId)
    objectAttributeValuePair = getObjectAttributeValuePairDB(objectId)

    for rule in rules:
        isPos = True

        ruleOperation = getRuleOperationDB(rule)
        if ruleOperation != operation:
            isPos = False
            continue
        ruleUserAttributeValuePair = getRuleUserAttributeValuePairDB(rule)
        for userAttr in ruleUserAttributeValuePair.keys():
            if userAttr in userAttributeValuePair.keys():
                if userAttributeValuePair[userAttr] != ruleUserAttributeValuePair[userAttr]:
                    isPos = False
                    break
            else:
                isPos = False
                break
        if isPos == False:
            continue
        ruleObjectAttributeValuePair = getRuleObjectAttributeValuePairDB(rule)
        for objectAttr in ruleObjectAttributeValuePair.keys():
            if objectAttr in objectAttributeValuePair.keys():
                if objectAttributeValuePair[objectAttr] != ruleObjectAttributeValuePair[objectAttr]:
                    isPos = False
                    break
            else:
                isPos = False
                break 
        if isPos == True:
            return True
    return False

if __name__ == "__main__":
    application.debug = True
    application.static_folder = 'static'
    application.run(threaded=True)   