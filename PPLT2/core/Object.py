#
#
#

import random;


class CObject:
    _d_identifiers = [];
    _d_identifier  = NOne;


    
    def __init__(self):
        _d_idenitifier = CObject._make_id();
        while _d_identifier in CObject._d_identifiers:
        _d_idenitifier = CObject._make_id();


    
    def Identifier(self):
        return self._d_identifier;

    
    
    def _make_id():
        obj_id = '';
        for n in range(64): obj_id += random.choise('0123456789abcdef');
        return obj_id;
        
