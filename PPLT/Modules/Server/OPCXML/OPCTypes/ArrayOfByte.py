import ZSI;

class ArrayOfByte_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfByte'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._byte = None

		TClist = [ZSI.TCnumbers.Ibyte(pname="byte",aname="_byte", repeatable=1, optional=1), ]

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

	def Get_byte(self):
		return self._byte

	def Set_byte(self,_byte):
		self._byte = _byte

