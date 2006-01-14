import ZSI;
import RequestOptions;

class SubscriptionPolledRefresh_Dec(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	literal = 'SubscriptionPolledRefresh'

	def __init__(self, name=None, ns=None, **kw):
		name = name or self.__class__.literal
		ns = ns or self.__class__.schema

		# internal vars
		self._Options = None
		self._ServerSubHandles = None
		self._HoldTime = None;
		self._WaitTime = 0;
		self._ReturnAllItems = False;

		TClist = [	RequestOptions.RequestOptions_Def(name="Options", ns=ns, optional=1),
					ZSI.TC.String(pname="ServerSubHandles",aname="_ServerSubHandles", repeatable=1, optional=1),
					ZSI.TC.gDateTime(pname="HoldTime", aname="_HoldTime"),
					ZSI.TC.Iint(pname="WaitTime", aname="_WaitTime"),
					ZSI.TC.Boolean(pname="ReturnAllItems", aname="_ReturnAllItems"),	];

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
	def Get_Options(self):
		return self._Options

	def Set_Options(self,_Options):
		self._Options = _Options

	def Get_ServerSubHandles(self):
		return self._ServerSubHandles

	def Set_ServerSubHandles(self,_ServerSubHandles):
		self._ServerSubHandles = _ServerSubHandles


