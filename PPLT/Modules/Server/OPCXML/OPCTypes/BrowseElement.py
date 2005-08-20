import ZSI;
import ItemProperty;

class BrowseElement_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'BrowseElement'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Properties = None
		self._Name = None;
		self._ItemPath = None;
		self._ItemName = None;
		self._IsItem = None;
		self._HasChildren = None;

		TClist = [	ItemProperty.ItemProperty_Def(name="Properties", ns=ns, repeatable=1, optional=1), 
					ZSI.TC.String(pname="Name", aname="_Name"),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),
					ZSI.TC.Boolean(pname="IsItem", aname="_IsItem", optional=0),
					ZSI.TC.Boolean(pname="HasChildren", aname="_HasChildren", optional=0),	]

		oname = name

		if name:
			aname = '_%s' % name
			if ns:
				oname += ' xmlns="%s"' % ns
			else:
				oname += ' xmlns="%s"' % self.__class__.schema
		else:
			aname = None

		ZSI.TCcompound.Struct.__init__(	self, self.__class__, TClist,
										pname=name, inorder=0,
										aname=aname, oname=oname,
										hasextras=1, **kw)


	def Get_Properties(self): return self._Properties;
	def Set_Properties(self,_Properties): self._Properties = _Properties;
	def Get_Name(self): return(self._Name);
	def Set_Name(self, Name): self._Name = Name;
	def Get_ItemPath(self): return(self._ItemPath);
	def Set_ItemPath(self, ItemPath): self._ItemPath = ItemPath;
	def Get_ItemName(self): return(self._ItemName);
	def Set_ItemName(self, ItemName): self._ItemName = ItemName;
	def Get_IsItem(self): return(self._IsItem);
	def Set_IsItem(self, IsItem): self._IsItem = IsItem;
	def Get_HasChildren(self): return(self._HasChildren);
	def Set_HasChildren(self, HasChildren): self._HasChildren = HasChildren;

