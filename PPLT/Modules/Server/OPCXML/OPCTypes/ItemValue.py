import ZSI;
import OPCQuality;



class ItemValue_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ItemValue'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._DiagnosticInfo = None
		self._Value = None
		self._Quality = None
		self._ValueTypeQualier = None;
		self._ItemPath = None;
		self._ItemName = None;
		self._ClientItemHandle = None;
		self._Timestamp = None;
		self._ResultID = None;


		TClist = [	ZSI.TC.String(pname="DiagnosticInfo",aname="_DiagnosticInfo", optional=1),
					ZSI.TC.Any(pname="Value",aname="_Value", optional=1),
					OPCQuality.OPCQuality_Def(name="Quality", ns=ns, optional=1),
					ZSI.TC.QName(pname="ValueTypeQualifier", aname="_ValueTypeQualifier"),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.gDateTime(pname="TimeStamp", qname="_TimeStamp"),
					ZSI.TC.QName(pname="ResultID", aname="_ResultID"),	];

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
	def Get_DiagnosticInfo(self):
		return self._DiagnosticInfo

	def Set_DiagnosticInfo(self,_DiagnosticInfo):
		self._DiagnosticInfo = _DiagnosticInfo

	def Get_Value(self):
		return self._Value

	def Set_Value(self,_Value):
		self._Value = _Value

	def Get_Quality(self):
		return self._Quality

	def Set_Quality(self,_Quality):
		self._Quality = _Quality

