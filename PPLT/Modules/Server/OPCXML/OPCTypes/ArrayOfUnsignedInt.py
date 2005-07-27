import ZSI;

class ArrayOfUnsignedInt_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfUnsignedInt'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._unsignedInt = None

		TClist = [ZSI.TCnumbers.IunsignedInt(pname="unsignedInt",aname="_unsignedInt", repeatable=1, optional=1), ]

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

	def Get_unsignedInt(self):
		return self._unsignedInt

	def Set_unsignedInt(self,_unsignedInt):
		self._unsignedInt = _unsignedInt

