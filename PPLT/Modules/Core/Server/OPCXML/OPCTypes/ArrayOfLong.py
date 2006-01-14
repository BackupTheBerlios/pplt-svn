import ZSI;

class ArrayOfLong_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfLong'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._long = None

		TClist = [ZSI.TCnumbers.Ilong(pname="long",aname="_long", repeatable=1, optional=1), ]

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
	
	def Get_long(self):
		return self._long

	def Set_long(self,_long):
		self._long = _long

