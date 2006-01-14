import ZSI;

class ArrayOfString_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfString'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._string = None

		TClist = [ZSI.TC.String(pname="string",aname="_string", repeatable=1, optional=1), ]

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

	def Get_string(self):
		return self._string

	def Set_string(self,_string):
		self._string = _string

