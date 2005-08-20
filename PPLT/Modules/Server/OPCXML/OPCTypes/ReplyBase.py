import ZSI;
import serverState;
from ZSIPatch import Struct;

class ReplyBase_Def(Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ReplyBase'

	def __init__(self, name=None, ns=None, **kw):

		self._RcvTime = None;
		self._ReplyTime = None;
		self._ClientRequestHandle = None;
		self._RevisedLocaleID = None;
		self._ServerState = None;

		AttrList = [	ZSI.TC.gDateTime(pname="RcvTime", aname="_RcvTime", optional=0),
						ZSI.TC.gDateTime(pname="ReplyTime", aname="_ReplyTime", optional=0),
						ZSI.TC.String(pname="ClientRequestHandle", aname="_ClientRequestHandle", optional=1),
						ZSI.TC.String(pname="RevisedLocaleID", aname="_RevisedLocaleID", optional=1),
						serverState.serverState_Def(name="ServerState", ns=ns, optional=0),	];
		TClist	= [];

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


	def Get_RcvTime(self): return(self._RcvTime);
	def Set_RcvTime(self, Time): self._RcvTime = Time;
	def Get_ReplyTime(self): return(self._ReplyTime);
	def Set_ReplyTime(self, Time): self._ReplyTime = Time;
	def Get_ClientRequestHandle(self): return(self._ClientRequestHandle);
	def Set_ClientRequestHandle(self, Handle): self._ClientRequestHandle = Handle;
	def Get_RevisedLocaleID(self): return(self._RevisedLocaleID);
	def Set_RevisedLocaleID(self, ID): self._RevisedLocaleID = ID;
	def Get_ServerState(self): return(self._ServerState);
	def Set_ServerState(self, State): self._ServerState = State;

