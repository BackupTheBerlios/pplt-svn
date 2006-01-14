import ZSI;

class ArrayOfUnsignedLong_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfUnsignedLong'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._unsignedLong = None

		TClist = [ZSI.TCnumbers.IunsignedLong(pname="unsignedLong",aname="_unsignedLong", repeatable=1, optional=1), ]

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

	def Get_unsignedLong(self):
		return self._unsignedLong

	def Set_unsignedLong(self,_unsignedLong):
		self._unsignedLong = _unsignedLong

