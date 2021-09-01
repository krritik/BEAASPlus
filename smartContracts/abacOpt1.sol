// ABAC State Smart Contract version-0.1.0
pragma solidity >=0.4.22 <0.8.0;

contract ABACOpt1 {
    // Variables to store user info
    bytes32 [] users;
    bytes32 [] userAttributes;
    mapping(bytes32 => bytes32[]) userAttributePosValues;
    mapping(bytes32 => mapping(bytes32 => bytes32)) userAttributeValuePair;

    // Variables to store object info
    bytes32 [] objects;
    bytes32 [] objectAttributes;
    mapping(bytes32 => bytes32[]) objectAttributePosValues;
    mapping(bytes32 => mapping(bytes32 => bytes32)) objectAttributeValuePair;

    // Variable to store operation 
    bytes32[] operations;

    // Variables to store policy info
    struct rule {
        mapping(bytes32 => bytes32) userAttribute;
        mapping(bytes32 => bytes32) objectAttribute;
        bytes32 operation;
    } 
    mapping(bytes32 => rule) rules;
    bytes32[] ruleIds;

    event accessRequestResponse(bytes32 indexed userId, bytes32 indexed objectId, bytes32 indexed operation, bool accessGiven);
    event accessibleObjectsReturned(bytes32 indexed userId, bytes32 indexed operation, bytes32[] objects);

    // Functions to modify user details in blockchain
    function addUsers(bytes32[] memory _U) public {
        for(uint i=0; i<_U.length; i++) {
            users.push(_U[i]);
        }
    }
    function addUserAttributes(bytes32[] memory _UA) public {
        for(uint i=0; i<_UA.length; i++) {
            userAttributes.push(_UA[i]);
        }
    }
    function addUserAttributePosValues(bytes32  _UA, bytes32[] memory _value) public {
        for(uint i=0; i<_value.length; i++) {
            userAttributePosValues[_UA].push(_value[i]);
        }
    }
    function addUserAttributeValuePair(bytes32  _U, bytes32[] memory _attr, bytes32[] memory _value) public {
        for(uint i=0; i<_attr.length; i++) {
            userAttributeValuePair[_U][_attr[i]] = _value[i];
        }
    }
    // Functions to get user details in blockchain
    function getUsers() public view returns(bytes32[] memory) {
        return users;
    }
    function getUserAttributes() public view returns(bytes32[] memory) {
        return userAttributes;
    }
    function getUserAttributePosValues(bytes32 _UA) public view returns(bytes32[] memory) {
        return userAttributePosValues[_UA];
    }
    function getUserAttributeValuePair(bytes32 _U) public view returns(bytes32[] memory, bytes32[] memory) {
        uint len = userAttributes.length;
        bytes32[] memory attr;
        bytes32[] memory values = new bytes32[](len);
        attr = userAttributes;
        for(uint i=0; i<len; i++) {
            values[i] = userAttributeValuePair[_U][attr[i]];
        }
        return (attr, values);
    }


    // Functions to modify object details in blockchain
    function addObjects(bytes32[] memory _O) public {
        for(uint i=0; i<_O.length; i++) {
            objects.push(_O[i]);
        }
    }
    function addObjectAttributes(bytes32[] memory _OA) public {
        for(uint i=0; i<_OA.length; i++) {
            objectAttributes.push(_OA[i]);
        }
    }
    function addObjectAttributePosValues(bytes32  _OA, bytes32[] memory _value) public {
        for(uint i=0; i<_value.length; i++) {
            objectAttributePosValues[_OA].push(_value[i]);
        }
    }
    function addObjectAttributeValuePair(bytes32  _O, bytes32[] memory _attr, bytes32[] memory _value) public {
        for(uint i=0; i<_attr.length; i++) {
            objectAttributeValuePair[_O][_attr[i]] = _value[i];
        }
    }
    // Functions to get object details in blockchain
    function getObjects() public view returns(bytes32[] memory) {
        return objects;
    }
    function getObjectAttributes() public view returns(bytes32[] memory) {
        return objectAttributes;
    }
    function getObjectAttributePosValues(bytes32 _OA) public view returns(bytes32[] memory) {
        return objectAttributePosValues[_OA];
    }
    function getObjectAttributeValuePair(bytes32 _O) public view returns(bytes32[] memory, bytes32[] memory) {
        uint len = objectAttributes.length;
        bytes32[] memory attr;
        bytes32[] memory values = new bytes32[](len);
        attr = objectAttributes;
        for(uint i=0; i<len; i++) {
            values[i] = objectAttributeValuePair[_O][attr[i]];
        }
        return (attr, values);
    }


    // Function for operations
    function addOperations(bytes32[] memory _OP) public {
        for(uint i=0; i<_OP.length; i++) {
            operations.push(_OP[i]);
        }
    }
    function getOperations() public view returns(bytes32[] memory) {
        return operations;
    }


    // Function to modify policy and rules in blockchain
    function addUserAttributeValuePairToRule(bytes32 _ruleId, bytes32[] memory _attr, bytes32[] memory _val) public{
        for(uint i=0; i<_attr.length; i++) {
            rules[_ruleId].userAttribute[_attr[i]] = _val[i];
        }
    }
    function addObjectAttributeValuePairToRule(bytes32 _ruleId, bytes32[] memory _attr, bytes32[] memory _val) public{
        for(uint i=0; i<_attr.length; i++) {
            rules[_ruleId].objectAttribute[_attr[i]] = _val[i];
        }
    }
    function addOperationToRule(bytes32 _ruleId, bytes32 _op) public {
        rules[_ruleId].operation = _op;
    }
    function addRules(bytes32[] memory _rules) public{
        for(uint i=0; i<_rules.length; i++) {
            ruleIds.push(_rules[i]);
        }
    }
    // Functions to get Policy and rule info
    function getRules() public view returns(bytes32[] memory) {
        return ruleIds;
    }
    function getUserAttributeValuePairFromRule(bytes32 _ruleId) public view returns(bytes32[] memory, bytes32[] memory) {
        uint len = userAttributes.length;
        bytes32[] memory attr;
        bytes32[] memory values = new bytes32[](len);
        attr = userAttributes;
        for(uint i=0; i<len; i++) {
            values[i] = rules[_ruleId].userAttribute[attr[i]];
        }
        return (attr, values);
    }
    function getObjectAttributeValuePairFromRule(bytes32 _ruleId) public view returns(bytes32[] memory, bytes32[] memory) {
        uint len = objectAttributes.length;
        bytes32[] memory attr;
        bytes32[] memory values = new bytes32[](len);
        attr = objectAttributes;
        for(uint i=0; i<len; i++) {
            values[i] = rules[_ruleId].objectAttribute[attr[i]];
        }
        return (attr, values);
    }
    function getOperationFromRule(bytes32 _ruleId) public view returns(bytes32) {
        return rules[_ruleId].operation;
    }

    // Functions to AccessRequests
    function accessRequestPerObject(bytes32 _userId, bytes32 _objectId, bytes32 _operation, bool _accessGiven) external {
        emit accessRequestResponse(_userId, _objectId, _operation, _accessGiven);
    }
    function getAccessibleObjects(bytes32 _userId, bytes32 _operation, bytes32[] calldata _objects) external {
        emit accessibleObjectsReturned(_userId, _operation, _objects);
    }
}