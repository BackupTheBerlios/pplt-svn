import ZSI;

class ArrayOfBoolean_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfBoolean'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._boolean = None

		TClist = [ZSI.TC.Boolean(pname="boolean",aname="_boolean", repeatable=1, optional=1), ]

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

	def Get_boolean(self):
		return self._boolean

	def Set_boolean(self,_boolean):
		self._boolean = _boolean

