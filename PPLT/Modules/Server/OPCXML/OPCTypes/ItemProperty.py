import ZSI;

class ItemProperty_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ItemProperty'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Value = None
		self._Name = None;
		self._Description = None;
		self._ItemPath = None;
		self._ItemName = None;
		self._ResultID = None;


		TClist = [	ZSI.TC.Any(pname="Value",aname="_Value", optional=1), 
					ZSI.TC.String(pname="Name", aname="_Name", optional=0),
					ZSI.TC.String(pname="Description", aname="_Description"),
					ZSI.TC.String(pname="ItemPath", aname="_ItemPath"),
					ZSI.TC.String(pname="ItemName", aname="_ItemName"),
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

	def Get_Value(self):
		return self._Value

	def Set_Value(self,_Value):
		self._Value = _Value

