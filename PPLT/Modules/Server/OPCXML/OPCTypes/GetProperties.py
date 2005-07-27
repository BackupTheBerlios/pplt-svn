import ZSI;
import ItemIdentifier;

class GetProperties_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'GetProperties'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._ItemIDs = None
		self._PropertyNames = None
		self._LocaleID = None;
		self._ClientRequestHandle = None;
		self._ItemPath = None;
		self._ReturnAllProperties = False;
		self._ReturnPropertyValues = False;
		self._ReturnErrorText = False;


		TClist = [	ItemIdentifier.ItemIdentifier_Def(name="ItemIDs", ns=ns, repeatable=1, optional=1),
					ZSI.TC.QName(pname="PropertyNames",aname="_PropertyNames", repeatable=1, optional=1),
					ZSI.TC.String(pname="LocaleID", aname="_LocaleID"),
					ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle"),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.Boolean(pname="ReturnAllProperties", aname="_ReturnAllProperties"),
					ZSI.TC.Boolean(pname="ReturnPropertyValues", aname="_ReturnPropertyValues"),
					ZSI.TC.Boolean(pname="ReturnErrorText", aname="_ReturnErrorText"),	];

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
	def Get_ItemIDs(self):
		return self._ItemIDs

	def Set_ItemIDs(self,_ItemIDs):
		self._ItemIDs = _ItemIDs

	def Get_PropertyNames(self):
		return self._PropertyNames

	def Set_PropertyNames(self,_PropertyNames):
		self._PropertyNames = _PropertyNames


