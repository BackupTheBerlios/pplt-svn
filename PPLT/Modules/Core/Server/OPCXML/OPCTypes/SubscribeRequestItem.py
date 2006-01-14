import ZSI;

class SubscribeRequestItem_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'SubscribeRequestItem'

	def __init__(self, name=None, ns=None, **kw):
		self._ItemPath = None;
		self._ReqType = None;
		self._ItemName = None;
		self._ClientItemHandle = None;
		self._Deadband = None;
		self._RequestedSamplingRate = None;
		self._EnableBuffering = None;

		TClist = [	ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.QName(pname="ReqType", aname="_ReqType"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),
					ZSI.TC.String(pname="ClientItemHandle", aname="_ClientItemHandle"),
					ZSI.TC.FPfloat(pname="Deadband", aname="_Deadband"),
					ZSI.TC.Iint(pname="RequestedSamplingRate", aname="_RequestedSamplingRate"),
					ZSI.TC.Boolean(pname="EnableBuffering", aname="_EnableBuffering"),	];


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


