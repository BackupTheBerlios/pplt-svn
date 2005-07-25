import logging;

class Version:
	def __init__(self, VerStr):
		self.__Logger = logging.getLogger("PPLT");
		self.__VersionString = VerStr;
		tmp = VerStr.split('.');
		self.__Version = [0, 0, 0];
#		self.__Logger.debug("Try to parse %s"%VerStr);
		#self.__PATCH  = 0;
		l = len(tmp);
		if l > 3: l = 3;
		for n in range(0,l):
			try:
				self.__Version[n] = int(tmp[n]);
			except:
				self.__Version[n] = 0;
#		self.__Logger.debug("Init verion %s"%hex(self));

	def GetMajor(self): return(self.__Version[0]);
	def GetMinor(self): return(self.__Version[1]);
	def GetBugFix(self): return(self.__Version[2]);
	def __int__(self):
		v = self.__Version[0];
		v = (v<<8)|self.__Version[1];
		v = (v<<16)|self.__Version[0];
		return(v);
	def __hex__(self): return(hex(self.__int__()));
	def __str__(self): return(self.__VersionString);
	def __eq__(self, other): return(int(self) == int(other));
	def __ne__(self, other): return(int(self) != int(other));
	def __cmp__(self, other): return(int(self)-int(other));

