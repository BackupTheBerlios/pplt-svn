import ZSI;
import ReplyBase;
import SubscribeReplyItemList;
import OPCError

class SubscribeResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'SubscribeResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._SubscribeResult = None
		self._RItemList = None
		self._Errors = None
		self._ServerSubHandle = None;


		TClist = [	ReplyBase.ReplyBase_Def(name="SubscribeResult", ns=ns, optional=1),
					SubscribeReplyItemList.SubscribeReplyItemList_Def(name="RItemList", ns=ns, optional=1),
					OPCError.OPCError_Def(name="Errors", ns=ns, repeatable=1, optional=1),
					ZSI.TC.String(pname="ServerSubHandle", aname="_ServerSubHandle"),	];

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

	def Get_SubscribeResult(self):
		return self._SubscribeResult

	def Set_SubscribeResult(self,_SubscribeResult):
		self._SubscribeResult = _SubscribeResult

	def Get_RItemList(self):
		return self._RItemList

	def Set_RItemList(self,_RItemList):
		self._RItemList = _RItemList

	def Get_Errors(self):
		return self._Errors

	def Set_Errors(self,_Errors):
		self._Errors = _Errors


