import ZSI;
import ReplyBase;
import ReplyItemList;
import OPCError;

class WriteResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'WriteResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._WriteResult = None
		self._RItemList = None
		self._Errors = None

		TClist = [	ReplyBase.ReplyBase_Def(name="WriteResult", ns=ns, optional=1),
					ReplyItemList.ReplyItemList_Def(name="RItemList", ns=ns, optional=1),
					OPCError.OPCError_Def(name="Errors", ns=ns, repeatable=1, optional=1),	];

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

	def Get_WriteResult(self):
		return self._WriteResult

	def Set_WriteResult(self,_WriteResult):
		self._WriteResult = _WriteResult

	def Get_RItemList(self):
		return self._RItemList

	def Set_RItemList(self,_RItemList):
		self._RItemList = _RItemList

	def Get_Errors(self):
		return self._Errors

	def Set_Errors(self,_Errors):
		self._Errors = _Errors

