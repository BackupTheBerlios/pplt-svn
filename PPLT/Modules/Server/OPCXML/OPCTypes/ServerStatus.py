import ZSI;
import interfaceVersion;

class ServerStatus_Def(ZSI.TCcompound.Struct):
	schema = 'http://opcfoundation.org/webservices/XMLDA/1.0/'
	type = 'ServerStatus'

	def __init__(self, name=None, ns=None, **kw):
		self._StatusInfo = None;
		self._VendorInfo = None;
		self._SupportedLocaleIDs = None;
		self._SupportedInterfaceVersions = None;
		self._ProductVersion = None;
		self._StartTime = None;

		TClist =	[ZSI.TC.String(pname="StatusInfo",aname="_StatusInfo", optional=1),
					ZSI.TC.String(pname="VendorInfo",aname="_VendorInfo", optional=1),
					ZSI.TC.String(pname="SupportedLocaleIDs",aname="_SupportedLocaleIDs", repeatable=1, optional=1),
					interfaceVersion.interfaceVersion_Def(name="SupportedInterfaceVersions",ns=ns, repeatable=1, optional=1),
					ZSI.TC.String(pname="ProductVersion", aname="_ProductVersion"),
					ZSI.TC.gDateTime(pname="StartTime",aname="_StartTime", optional=0),	]

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
		def Get_StatusInfo(self):
			return self._StatusInfo

		def Set_StatusInfo(self,_StatusInfo):
			self._StatusInfo = _StatusInfo

		def Get_VendorInfo(self):
			return self._VendorInfo

		def Set_VendorInfo(self,_VendorInfo):
			self._VendorInfo = _VendorInfo

		def Get_SupportedLocaleIDs(self):
			return self._SupportedLocaleIDs

		def Set_SupportedLocaleIDs(self,_SupportedLocaleIDs):
			self._SupportedLocaleIDs = _SupportedLocaleIDs

		def Get_SupportedInterfaceVersions(self):
			return self._SupportedInterfaceVersions

		def Set_SupportedInterfaceVersions(self,_SupportedInterfaceVersions):
			self._SupportedInterfaceVersions = _SupportedInterfaceVersions

		def Set_ProductVersion(self, Version):
			self._ProductVersion = Version;

		def Get_ProductVersion(self):
			return self._ProductVersion;

		def Set_StartTime(self, StartTime):
			self._StartTime = StartTime;

		def Get_StartTime(self):
			return self._StartTime;


