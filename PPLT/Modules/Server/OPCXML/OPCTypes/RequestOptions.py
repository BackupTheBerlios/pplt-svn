import ZSI;


class RequestOptions_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'RequestOptions'

	def __init__(self, name=None, ns=None, **kw):

		self._ReturnErrorText = True;
		self._ReturnDiagnosticInfo = False;
		self._ReturnItemTime = False;
		self._ReturnItemPath = False;
		self._ReturnItemName = False;
		self._RequestDeadline = None;
		self._ClientRequestHandle = None;
		self._LocaleID = None;

		TClist = [	ZSI.TC.Boolean(pname="ReturnErrorText", aname="_ReturnErrorText"),
					ZSI.TC.Boolean(pname="ReturnDiagnosticInfo", aname="_ReturnDiagnosticInfo"),
					ZSI.TC.Boolean(pname="ReturnItemTime", aname="_ReturnItemTime"),
					ZSI.TC.Boolean(pname="ReturnItemPath", aname="_ReturnItemPath"),
					ZSI.TC.Boolean(pname="ReturnItemName", aname="_ReturnItemName"),
					ZSI.TC.gDateTime(pname="RequestDeadline", aname="_RequestDeadline", optional=0),
					ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle", optional=0),	];

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

