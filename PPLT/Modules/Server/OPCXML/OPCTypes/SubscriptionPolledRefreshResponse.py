import ZSI;
import ReplyBase;
import SubscribePolledRefreshReplyItemList;
import OPCError;

class SubscriptionPolledRefreshResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'SubscriptionPolledRefreshResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._SubscriptionPolledRefreshResult = None
		self._InvalidServerSubHandles = None
		self._RItemList = None
		self._Errors = None
		self._DataBufferOverflow = False;

		TClist = [	ReplyBase.ReplyBase_Def(name="SubscriptionPolledRefreshResult", ns=ns, optional=1),
					ZSI.TC.String(pname="InvalidServerSubHandles",aname="_InvalidServerSubHandles", repeatable=1, optional=1),
					SubscribePolledRefreshReplyItemList.SubscribePolledRefreshReplyItemList_Def(name="RItemList", ns=ns, repeatable=1, optional=1),
					OPCError.OPCError_Def(name="Errors", ns=ns, repeatable=1, optional=1),
					ZSI.TC.Boolean(pname="DataBufferOverflow", aname="_DataBufferOverflow"),	];

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

	def Get_SubscriptionPolledRefreshResult(self):
		return self._SubscriptionPolledRefreshResult

	def Set_SubscriptionPolledRefreshResult(self,_SubscriptionPolledRefreshResult):
		self._SubscriptionPolledRefreshResult = _SubscriptionPolledRefreshResult

	def Get_InvalidServerSubHandles(self):
		return self._InvalidServerSubHandles

	def Set_InvalidServerSubHandles(self,_InvalidServerSubHandles):
		self._InvalidServerSubHandles = _InvalidServerSubHandles

	def Get_RItemList(self):
		return self._RItemList

	def Set_RItemList(self,_RItemList):
		self._RItemList = _RItemList

	def Get_Errors(self):
		return self._Errors

	def Set_Errors(self,_Errors):
		self._Errors = _Errors


