import mysql.connector
from ABACblockchain import *
import threading


## default values ##
_host="localhost"
_port = 3306
_user="admin"
_password="abac@123"
_database="db1"

def updateDatabaseDetails(host, port, user, password, database):
    global _host, _port, _user, _password, _database
    _host = host
    _port = port
    _user = user
    _password = password
    _database = database


def initialDatabase():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password)
    mycursor = mydb.cursor()
    mycursor.execute('CREATE DATABASE IF NOT EXISTS db1')
    mycursor.execute('USE db1')
    mycursor.execute("CREATE TABLE IF NOT EXISTS Users(userId VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS UserAttributes(userAttributeName VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS UserAttributePosValues(userAttributeName VARCHAR(20), userAttributeValue VARCHAR(20), PRIMARY KEY(userAttributeName, userAttributeValue), FOREIGN KEY(userAttributeName) REFERENCES UserAttributes(userAttributeName))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS UserAttributeValuePair(userId VARCHAR(20), userAttributeName VARCHAR(20), userAttributeValue VARCHAR(20) NOT NULL, PRIMARY KEY(userId, userAttributeName), FOREIGN KEY(userId) REFERENCES Users(userId), FOREIGN KEY(userAttributeName, userAttributeValue) REFERENCES UserAttributePosValues(userAttributeName, userAttributeValue))")
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS Objects(objectId VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS ObjectAttributes(objectAttributeName VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS ObjectAttributePosValues(objectAttributeName VARCHAR(20), objectAttributeValue VARCHAR(20), PRIMARY KEY(objectAttributeName, objectAttributeValue), FOREIGN KEY(objectAttributeName) REFERENCES ObjectAttributes(objectAttributeName))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS ObjectAttributeValuePair(objectId VARCHAR(20), objectAttributeName VARCHAR(20), objectAttributeValue VARCHAR(20) NOT NULL, PRIMARY KEY(objectId, objectAttributeName), FOREIGN KEY(objectId) REFERENCES Objects(objectId), FOREIGN KEY(objectAttributeName, objectAttributeValue) REFERENCES ObjectAttributePosValues(objectAttributeName, objectAttributeValue))")
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS Operations(operation VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Rules(ruleId VARCHAR(20) PRIMARY KEY)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS RuleOperation(ruleId VARCHAR(20), operation VARCHAR(20) NOT NULL, PRIMARY KEY(ruleId), FOREIGN KEY(ruleId) REFERENCES Rules(ruleId), FOREIGN KEY(operation) REFERENCES Operations(operation))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS RuleUser(ruleId VARCHAR(20), userAttributeName VARCHAR(20), userAttributeValue VARCHAR(20) NOT NULL, PRIMARY KEY(ruleId, userAttributeName), FOREIGN KEY(ruleId) REFERENCES Rules(ruleId), FOREIGN KEY(userAttributeName, userAttributeValue) REFERENCES UserAttributePosValues(userAttributeName, userAttributeValue))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS RuleObject(ruleId VARCHAR(20), objectAttributeName VARCHAR(20), objectAttributeValue VARCHAR(20) NOT NULL, PRIMARY KEY(ruleId, objectAttributeName), FOREIGN KEY(ruleId) REFERENCES Rules(ruleId), FOREIGN KEY(objectAttributeName, objectAttributeValue) REFERENCES ObjectAttributePosValues(objectAttributeName, objectAttributeValue))")
    mydb.commit()


# // Functions to add User Attributes and Values    
def insertUsersDB(users):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for user in users:
        mycursor.execute('INSERT INTO Users(userId) VALUES("%s")' %(user))
    mydb.commit()  
    insertUsersBC(users)
    t1 = threading.Thread(target=insertUsersBC, args=(users,))
    t1.start() 
    return

def insertUserAttributesDB(attrs):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for _attr in attrs:
        mycursor.execute('INSERT INTO UserAttributes(userAttributeName) VALUES ("%s")' %(_attr))
    mydb.commit()
    insertUserAttributesBC(attrs)
    t1 = threading.Thread(target=insertUserAttributesBC, args=(attrs,))
    t1.start()
    return

def insertUserAttributePosValuesDB(attrName, attrValues):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for value in attrValues:
        mycursor.execute('INSERT INTO UserAttributePosValues(userAttributeName, userAttributeValue) VALUES ("%s", "%s")' %(attrName, value))
    mydb.commit()
    insertUserAttributePosValuesBC(attrName, attrValues)  
    t1 = threading.Thread(target=insertUserAttributePosValuesBC, args=(attrName, attrValues))
    t1.start() 
    return

def insertUserAttributeValuePairDB(userId, attrValuePair):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for attr, value in attrValuePair.items():
        mycursor.execute('INSERT INTO UserAttributeValuePair(userId, userAttributeName, userAttributeValue) VALUES ("%s", "%s", "%s")' %(userId, attr, value))
    mydb.commit()
    attrs = attrValuePair.keys()
    values = attrValuePair.values()
    insertUserAttributeValuePairBC(userId, attrs, values)
    t1 = threading.Thread(target=insertUserAttributeValuePairBC, args=(userId, attrs, values))
    t1.start() 
    return

def getUsersDB():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT userId from Users') 
    data = mycursor.fetchall()
    users = [x[0] for x in data]
    return users 

def getUserAttributesDB():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT userAttributeName FROM UserAttributes')
    data = mycursor.fetchall()
    userAttributes = [x[0] for x in data]
    return userAttributes

def getUserAttributePosValuesDB(attrName):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT userAttributeValue FROM UserAttributePosValues where userAttributeName = "%s"' %(attrName))
    data = mycursor.fetchall()
    userAttributes = [x[0] for x in data]
    return userAttributes

def getUserAttributeValuePairDB(userId):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT userAttributeName, userAttributeValue FROM UserAttributeValuePair where userId = "%s"' %(userId))
    data = mycursor.fetchall()
    attributeValuePair = {}
    for x in data:
        attrName = x[0]
        attrValue = x[1]
        attributeValuePair[attrName] = attrValue
    return attributeValuePair


# // Functions to add Object Attributes and Values  
def insertObjectsDB(objects):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for object in objects:
        mycursor.execute('INSERT INTO Objects(objectId) VALUES("%s")' %(object))
    mydb.commit()  
    insertObjectsBC(objects)  

def insertObjectAttributesDB(attrs):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for _attr in attrs:
        mycursor.execute('INSERT INTO ObjectAttributes(objectAttributeName) VALUES ("%s")' %(_attr))
    mydb.commit()
    insertObjectAttributesBC(attrs)

def insertObjectAttributePosValuesDB(attrName, attrValues):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for value in attrValues:
        mycursor.execute('INSERT INTO ObjectAttributePosValues(objectAttributeName, objectAttributeValue) VALUES ("%s", "%s")' %(attrName, value))
    mydb.commit()
    insertObjectAttributePosValuesBC(attrName, attrValues)

def insertObjectAttributeValuePairDB(objectId, attrValuePair):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for attr, value in attrValuePair.items():
        mycursor.execute('INSERT INTO ObjectAttributeValuePair(objectId, objectAttributeName, objectAttributeValue) VALUES ("%s", "%s", "%s")' %(objectId, attr, value))
    mydb.commit()
    attrs = attrValuePair.keys()
    values = attrValuePair.values()
    insertObjectAttributeValuePairBC(objectId, attrs, values)
   

def getObjectsDB():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT objectId from Objects') 
    data = mycursor.fetchall()
    objects = [x[0] for x in data]
    return objects 

def getObjectAttributesDB():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT objectAttributeName FROM ObjectAttributes')
    data = mycursor.fetchall()
    objectAttributes = [x[0] for x in data]
    return objectAttributes

def getObjectAttributePosValuesDB(attrName):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT objectAttributeValue FROM ObjectAttributePosValues where objectAttributeName = "%s"' %(attrName))
    data = mycursor.fetchall()
    objectAttributes = [x[0] for x in data]
    return objectAttributes

def getObjectAttributeValuePairDB(objectId):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT objectAttributeName, objectAttributeValue FROM ObjectAttributeValuePair where objectId = "%s"' %(objectId))
    data = mycursor.fetchall()
    attributeValuePair = {}
    for x in data:
        attrName = x[0]
        attrValue = x[1]
        attributeValuePair[attrName] = attrValue
    return attributeValuePair


# // Functions to add Operations
def insertOperationsDB(operations):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for operation in operations:
        mycursor.execute('INSERT INTO Operations(operation) VALUES("%s")' %(operation))
    mydb.commit()
    insertOperationsBC(operations)

def getOperationsDB():    
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT operation FROM Operations')
    data = mycursor.fetchall()
    objectAttributes = [x[0] for x in data]
    return objectAttributes



# // Functions to add Rules 
def insertRulesDB(rules):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    for rule in rules:
        mycursor.execute('INSERT INTO Rules(ruleId) VALUES("%s")' %(rule))
    mydb.commit()
    insertRulesBC(rules)

def insertRuleOperationDB(ruleId, operation):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('INSERT INTO RuleOperation(ruleId, operation) VALUES("%s", "%s")' %(ruleId, operation))
    mydb.commit() 
    insertOperationToRuleBC(ruleId, operation)

def insertRuleUserDB(ruleId, userAttrValuePair):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for attr, value in userAttrValuePair.items():
        mycursor.execute('INSERT INTO RuleUser(ruleId, userAttributeName, userAttributeValue) VALUES ("%s", "%s", "%s")' %(ruleId, attr, value))
    mydb.commit()
    attrs = userAttrValuePair.keys()
    values = userAttrValuePair.values()
    insertUserAttributeValuePairToRuleBC(ruleId, attrs, values)
   
def insertRuleObjectDB(ruleId, objectAttrValuePair):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    for attr, value in objectAttrValuePair.items():
        mycursor.execute('INSERT INTO RuleObject(ruleId, objectAttributeName, objectAttributeValue) VALUES ("%s", "%s", "%s")' %(ruleId, attr, value))
    mydb.commit()
    attrs =objectAttrValuePair.keys()
    values = objectAttrValuePair.values()
    insertObjectAttributeValuePairToRuleBC(ruleId, attrs, values)

def getRulesDB():
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT ruleId FROM Rules')
    data = mycursor.fetchall()
    rules = [x[0] for x in data]
    return rules

def getRuleOperationDB(ruleId):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT operation FROM RuleOperation where ruleId = "%s"' %(ruleId))
    data = mycursor.fetchall()
    operation = data[0][0]
    return operation    

def getRuleUserAttributeValuePairDB(ruleId):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT userAttributeName, userAttributeValue FROM RuleUser where ruleId = "%s"' %(ruleId))
    data = mycursor.fetchall()
    attributeValuePair = {}
    for x in data:
        attrName = x[0]
        attrValue = x[1]
        attributeValuePair[attrName] = attrValue
    return attributeValuePair

def getRuleObjectAttributeValuePairDB(ruleId):
    mydb = mysql.connector.connect(host=_host, port=_port, user=_user, password=_password, database=_database)
    mycursor = mydb.cursor()  
    mycursor.execute('SELECT objectAttributeName, objectAttributeValue FROM RuleObject where ruleId = "%s"' %(ruleId))
    data = mycursor.fetchall()
    attributeValuePair = {}
    for x in data:
        attrName = x[0]
        attrValue = x[1]
        attributeValuePair[attrName] = attrValue
    return attributeValuePair