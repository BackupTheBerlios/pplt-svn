import ZSI;

class ReadRequestItem_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ReadRequestItem'

	def __init__(self, name=None, ns=None, **kw):

		self._ItemPath = None;
		self._ReqType = None;
		self._ItemName = None;
		self._ClientItemHandle = None;
		self._MaxAge = None;

		TClist = [	ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
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

		ZSI.TCcompound.Struct.__init__(	self, self.__class__, TClist,
										pname=name, inorder=0,
										aname=aname, oname=oname,
										**kw)

