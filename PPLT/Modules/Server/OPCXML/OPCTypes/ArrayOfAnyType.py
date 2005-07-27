import ZSI;

class ArrayOfAnyType_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfAnyType'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._anyType = None

		TClist = [ns1.anyType_Def(name="anyType",ns=ns, repeatable=1, optional=1), ]

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

	def Get_anyType(self):
		return self._anyType

	def Set_anyType(self,_anyType):
		self._anyType = _anyType

