class AliasTable:
    def __init__(self):
        self.__Table = {};

    def GetAlias(self, ID):
        items = self.__Table.items();
        for item in items:
            if ID == item[1]:
                return(item[0]);
        return(None);

    def GetID(self, Alias):
        return(self.__Table.get(Alias));

    def Add(self, Alias, ID):
        if self.__Table.has_key(Alias):
            return(False);
        self.__Table.update( {Alias:ID} );
        return(True);

    def DelID(self, ID):
        Alias = self.GetAlias(ID);
        if not Alias:
            return(False);
        del self.__Table[Alias];
        return(True);

    def DelAlias(self, Alias):
        if not self.__Table.has_key(Alias):
            return(False);
        del self.__Table[Alias];
        return(True);

    
