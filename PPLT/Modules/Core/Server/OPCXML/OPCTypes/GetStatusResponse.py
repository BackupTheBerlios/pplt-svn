import ZSI;
import ReplyBase;
import ServerStatus;

class GetStatusResponse_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'GetStatusResponse'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._GetStatusResult = None
		self._Status = None

		TClist = [	ReplyBase.ReplyBase_Def(name="GetStatusResult", ns=ns, optional=1),
					ServerStatus.ServerStatus_Def(name="Status", ns=ns, optional=1),	];

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

	def Get_GetStatusResult(self):
		return self._GetStatusResult

	def Set_GetStatusResult(self,_GetStatusResult):
		self._GetStatusResult = _GetStatusResult

	def Get_Status(self):
		return self._Status

	def Set_Status(self,_Status):
		self._Status = _Status
 
