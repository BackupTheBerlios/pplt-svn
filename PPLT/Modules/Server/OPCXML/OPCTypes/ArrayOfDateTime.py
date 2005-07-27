import ZSI;

class ArrayOfDateTime_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ArrayOfDateTime'

	def __init__(self, name=None, ns=None, **kw):
		# internal vars
		self._dateTime = None

		TClist = [ZSI.TCtimes.gDateTime(pname="dateTime",aname="_dateTime", repeatable=1, optional=1), ]

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

	def Get_dateTime(self):
		return self._dateTime

	def Set_dateTime(self,_dateTime):
		self._dateTime = _dateTime
 
