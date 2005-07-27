import ZSI;
import ReplyBase;
import PropertyReplyList;
import OPCError;

class GetPropertiesResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'GetPropertiesResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._GetPropertiesResult = None
		self._PropertyLists = None
		self._Errors = None

		TClist = [	ReplyBase.ReplyBase_Def(name="GetPropertiesResult", ns=ns, optional=1),
					PropertyReplyList.PropertyReplyList_Def(name="PropertyLists", ns=ns, repeatable=1, optional=1),
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

	
	def Get_GetPropertiesResult(self):
		return self._GetPropertiesResult

	def Set_GetPropertiesResult(self,_GetPropertiesResult):
		self._GetPropertiesResult = _GetPropertiesResult

	def Get_PropertyLists(self):
		return self._PropertyLists

	def Set_PropertyLists(self,_PropertyLists):
		self._PropertyLists = _PropertyLists

	def Get_Errors(self):
		return self._Errors

	def Set_Errors(self,_Errors):
		self._Errors = _Errors


