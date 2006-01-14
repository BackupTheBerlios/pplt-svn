import ZSI;

class OPCError_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'OPCError'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._Text = None
		self._ID = None;

		TClist = [	ZSI.TC.String(pname="Text",aname="_Text", optional=1),
					ZSI.TC.QName(pname="ID", aname="_ID", optional=0),	];

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

	def Get_Text(self):
		return self._Text

	def Set_Text(self,_Text):
		self._Text = _Text


