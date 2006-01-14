import ZSI;
from ZSIPatch import Struct


class GetStatus_Dec(Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'GetStatus'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		self._LocaleID = None;
		self._ClientRequestHandle = None;

		TClist = [];
		AttrList = [	ZSI.TC.String(pname="LocaleID", aname="_LocaleID"),
						ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle"),	];

		oname = name

		if name:
			aname = '_%s' % name
			if ns:
				oname += ' xmlns="%s"' % ns
			else:
				oname += ' xmlns="%s"' % self.__class__.schema
		else:
			aname = None

		Struct.__init__(	self, self.__class__, TClist, AttrList,
							pname=name, inorder=0,
							aname=aname, oname=oname,
							**kw)

	def Get_LocaleID(self):
		return(self._LocaleID);
	def Set_LocaleID(sefl, ID): self._LocaleID = ID;
	def Get_ClientRequestHandle(self): return(self._ClientRequestHandle);
	def Set_ClientRequestHandle(self, Handle): self._ClientRequestHandle = Handle;

