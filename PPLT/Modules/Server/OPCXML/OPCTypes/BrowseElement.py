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


	def Get_Properties(self):
		return self._Properties

	def Set_Properties(self,_Properties):
		self._Properties = _Properties

