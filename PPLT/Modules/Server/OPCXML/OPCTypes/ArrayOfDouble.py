import ZSI;

class ArrayOfDouble_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfDouble'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._double = None

		TClist = [ZSI.TCnumbers.FPdouble(pname="double",aname="_double", repeatable=1, optional=1), ]

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
	def Get_double(self):
		return self._double

	def Set_double(self,_double):
		self._double = _double

