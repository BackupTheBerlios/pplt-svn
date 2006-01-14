import ZSI;
from ZSIPatch import Struct;

class ReadRequestItem_Def(Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ReadRequestItem'

	def __init__(self, name=None, ns=None, **kw):

		self._ItemPath = None;
		self._ReqType = None;
		self._ItemName = None;
		self._ClientItemHandle = None;
		self._MaxAge = None;

		TClist =	[];

		AttrList =	[ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.QName(pname="ReqType", aname="_ReqType"),
					ZSI.TC.String(pname="ClientItemHandle", aname="_ClientItemHandle"),
					ZSI.TC.Iint(pname="MaxAge", aname="_MaxAge"),	];

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

