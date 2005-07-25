

class InstallSource:
	def __init__(self, Lang, AltLang):
		self.Lang = Lang;
		self.AltLang = AltLang
		self.CoreDB = SourceClass();
		self.SrvDB	= SourceClass();
		self.DevDB	= SourceClass();

	def Load(self, Parameters):
		pass;

	def _AddCoreItem(self, Item, FQName):
		tmp = FQName.split(".");
		Name = tmp[-1];
		ClassLst = tmp[:-1];
		return(self.__CoreDB.AddItem(Item,ClassLst));

	def _AddSrvItem(self, Item, FQName):
		tmp = FQName.split(".");
		Name = tmp[-1];
		ClassLst = tmp[:-1];
		return(self.__SrvDB.AddItem(Item,ClassLst));

	def _AddDevItem(self, Item, FQName):
		tmp = FQName.split(".");
		Name = tmp[-1];
		ClassLst = tmp[:-1];
		return(self.__DevDB.AddItem(Item,ClassLst));

class SourceClass:
	def __init__(self, ClassName=None):
		self.__ClassName = ClassName;
		self.__Items = {};
		self.__SubClasses = {};
	
	def ListSubClasses(self): return(self.__SubClasses.keys());
	def ListItems(self): return(self.__Items.keys());
	def GetName(self): return(self.__ClassName);

	def AddItem(self, Item, ClassLst):
		if len(ClassLst) == 0:
			self.__Items.update( {Item.GetName():Item} );
			return(True);
		SubClass = ClassLst.pop(0);
		if not self.__SubClasses.has_key(SubClass):
			self.__SubClasses[SubClass] = SourceClass(SubClass);
		return(self.__SubClasses[SubClass].AddItem(ClassLst));
	
	def GetItem(self, Name, ClassLst):
		if len(ClassLst) == 0:
			return(self.__Items.get(Name));
		SubClass = ClassLst.pop(0);
		if not self.__SubClasses.has_key(SubClass):
			return(None);
		return(self.__SubClasses[SubClass].GetItem(Name,SubClass));


class SourceItem:
	def __init__(self, File, Name, Version, Description):
		self.__Name = Name;
		self.__Version = Version;
		self.__FileName = File;
		self.__Description = Description;

	def GetName(self): return(self.__Name);
	def GetVersion(self): return(self.__Version);
	def GetFile(self): return(self.__FileName);
	def GetDescription(self): return(self.__Description);

