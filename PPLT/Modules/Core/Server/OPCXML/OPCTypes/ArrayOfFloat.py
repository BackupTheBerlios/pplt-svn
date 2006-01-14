import ZSI;

class ArrayOfFloat_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfFloat'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._float = None

		TClist = [ZSI.TCnumbers.FPfloat(pname="float",aname="_float", repeatable=1, optional=1), ]

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

	def Get_float(self):
		return self._float

	def Set_float(self,_float):
		self._float = _float

