import ZSI;

class ArrayOfDecimal_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfDecimal'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._decimal = None

		TClist = [ZSI.TC.Decimal(pname="decimal",aname="_decimal", repeatable=1, optional=1), ]

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

	def Get_decimal(self):
		return self._decimal

	def Set_decimal(self,_decimal):
		self._decimal = _decimal

