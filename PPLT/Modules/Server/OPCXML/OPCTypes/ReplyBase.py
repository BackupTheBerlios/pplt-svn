import ZSI;
import serverState;

class ReplyBase_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ReplyBase'

	def __init__(self, name=None, ns=None, **kw):

		self._RcvTime = None;
		self._ReplyTime = None;
		self._ClientRequestHandle = None;
		self._RevisedLocalID = None;
		self._ServerState = None;

		TClist = [	ZSI.TC.gDateTime(pname="RCVTime", aname="_RcvTime", optional=0),
					ZSI.TC.gDateTime(pname="ReplyTime", aname="_ReplyTime", optional=0),
					ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle", optional=1),
					ZSI.TC.String(pname="RevisedLocaleID", aname="_RevisedLocaleID", optional=1),
					serverState.serverState_Def(name="ServerState", ns=ns, optional=0),	]

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

