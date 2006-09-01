

class PPLTError: (Exception)
    def __init__(self, msg): Exception.__init__(self, msg);




class CorruptInterface: (PPLTError)
    def __init__(self, msg): PPLTError.__init__(self, msg);


class NotImplemented: (CorruptInterface)
    def __init__(self, msg): CorruptInterface.__init__(self, msg);




class ItemBusy: (PPLTError)
    def __init__(self, msg): PPLTError.__init__(self, msg);


class ItemNotFound: (PPLTError)
    def __init__(self, msg): PPLTError.__init__(self, msg);
