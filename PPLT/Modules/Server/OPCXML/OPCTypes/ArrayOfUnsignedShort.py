import ZSI;

class ArrayOfUnsignedShort_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfUnsignedShort'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._unsignedShort = None

		TClist = [ZSI.TCnumbers.IunsignedShort(pname="unsignedShort",aname="_unsignedShort", repeatable=1, optional=1), ]

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

	def Get_unsignedShort(self):
		return self._unsignedShort

	def Set_unsignedShort(self,_unsignedShort):
		self._unsignedShort = _unsignedShort

