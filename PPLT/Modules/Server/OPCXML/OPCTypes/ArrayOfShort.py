import ZSI;

class ArrayOfShort_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfShort'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._short = None

		TClist = [ZSI.TCnumbers.Ishort(pname="short",aname="_short", repeatable=1, optional=1), ]

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

	def Get_short(self):
		return self._short

	def Set_short(self,_short):
		self._short = _short

