import ZSI;
import BrowseFilter;

class Browse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'Browse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._PropertyNames = None
		self._LocalID = None;
		self._ClientRequestHandle = None;
		self._ItemPath = None;
		self._ItemName = None;
		self._ContinuationPoint = None;
		self._MaxElementsReturned = 0;
		self._BrowseFilter = "all";
		self._ElementNameFilter = None;
		self._VendorFilter = None;
		self._ReturnAllPropertys = False;
		self._ReturnPropertyValues = False;
		self._ReturnErrorText = False;

		
		TClist = [	ZSI.TC.QName(pname="PropertyNames",aname="_PropertyNames", repeatable=1, optional=1),
					ZSI.TC.String(pname="LocalID", aname="_LocalID"),
					ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle"),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),
					ZSI.TC.String(pname="ContinuationPoint", aname="_ContinuationPoint"),
					ZSI.TC.Iint(pname="MaxElementsReturned", aname="_MaxElementsReturned"),
					BrowseFilter.browseFilter_Def(name="BrowseFilter"),
					ZSI.TC.String(pname="ElementNameFilter", aname="_ElementNameFilter"),
					ZSI.TC.String(pname="VendorFilter", aname="_VendorFilter"),
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

	def Get_PropertyNames(self):
		return self._PropertyNames

	def Set_PropertyNames(self,_PropertyNames):
		self._PropertyNames = _PropertyNames

