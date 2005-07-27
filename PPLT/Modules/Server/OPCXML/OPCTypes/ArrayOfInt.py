import ZSI;

class ArrayOfInt_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfInt'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._int = None

		TClist = [ZSI.TCnumbers.Iint(pname="int",aname="_int", repeatable=1, optional=1), ]

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

	def Get_int(self):
		return self._int

	def Set_int(self,_int):
		self._int = _int

