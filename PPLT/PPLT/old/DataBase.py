# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for industrial        #
# communication.                                                              #
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #

# Changelog:
# 2005-06-05:
#	Add version-control
# 2005-05-27:
#	Release as version 0.2.0

import xml.dom.minidom;
import glob;
import logging;
import pyDCPU;
import os;
import fnmatch;
import string;


TYPE_SERVER = 1;
TYPE_DEVICE = 2;
TYPE_COREMOD= 3;


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



class DBObjBaseClass:
	def __init__(self, FileName):
		self.__Logger = logging.getLogger("PPLT");
		self.__Require = [];
		if not self.parseFile(FileName):
			raise Exception("Error while parse File \"%s\""%FileName);
	
	def parseFile(self, FileName):
		# save FileName
		self.__FileName = FileName;

		# parese file and get RootElement
		try:
			doc = xml.dom.minidom.parse(FileName);
		except:
			self.__Logger.error("Error while parse file %s"%FileName);
			return(False);
		obj = doc.documentElement;
		
		# get name
		self.__Name = obj.attributes['name'].value;
		# get version: 
		self.__VersionString = str(obj.getAttribute("version"));
		if self.__VersionString == "None":
			self.__Logger.warning("Please get the new ModulePackage from http://pplt.berlios.de");
			self.__VersionString = "0.0.0";
		self.__Version = Version(self.__VersionString);

		# try to find out what type the file describe
		if obj.localName == 'PPLTDevice':
			self.__Type = TYPE_DEVICE;
		elif obj.localName == 'PPLTServer':
			self.__Type = TYPE_SERVER;
		else:
			return(False);

		# save class names and put them into a list
		classes = obj.attributes['class'].value;
		tmp_lst = classes.split('.');
		self.__ClassList = [];
		for classname in tmp_lst:
			if classname != '':
				self.__ClassList.append(classname);
		
		reqs = doc.getElementsByTagName("DCPUModule")
		for req_node in reqs:
			try:
				mod = str(req_node.firstChild.data);
				self.__Require.append(mod);
			except:
				continue;

		doc.unlink();
		return(True);
	
	def GetType(self):
		return(self.__Type);
	def GetClassList(self):
		return(self.__ClassList);
	def GetName(self):
		return(self.__Name);
	def GetFileName(self):
		return(self.__FileName);
	def GetVersion(self):
		return(self.__Version);
	def GetVersionString(self):
		return(self.__VersionString);
	def GetRequirements(self): return(self.__Require);



class DBCoreObjClass(DBObjBaseClass):
	def __init__(self, FileName, Class, Name):
		self.__Logger = logging.getLogger("PPLT");
		self.__ClassList = Class;
		self.__Name = Name
		self.__FileName = FileName;

		if not self.parseFile(self.__FileName):
			raise Exception("Error while parse file...");
		#self.__Logger.debug("Core-Module %s(%s) added to %s"%(Name, FileName, str(Class)));

	def parseFile(self, FileName):
		#self.__Logger.debug("Inspect %s"%FileName);
		try:
			META = pyDCPU.Modules.CoreModuleInfo.MetaData(FileName);
		except:
			self.__Logger.error("While open/parse meta.xml in %s"%FileName);
			return(False);
		self.__Type = TYPE_COREMOD;
		self.__VersionString = META.GetVersionString();
		self.__Version = Version(self.__VersionString);
		#check content;
		if not META.CheckDCPUVersion():
			self.__Logger.error("Invalid pyDCPU Version: please get the new.");
			return(False);
		if not META.CheckPythonVersion():
			self.__Logger.error("Invalid Python Verion...");
			return(False);
		if not META.CheckPythonModules():
			self.__Logger.error("One ore more Python libraries missed.");
			return(False);
		return(True);

	def GetClassList(self): return(self.__ClassList);
	def GetType(self): return(self.__Type);
	def GetName(self): return(self.__Name);
	def GetFileName(self): return(self.__FileName);
	def GetVersion(self): return(self.__Version);
	def GetVersionString(self): return(self.__VersionString);



class ObjClassContainer:
	def __init__(self, Parent, Name):
		self.__Parent = Parent;
		self.__Name = Name;
		self.__SubClassList = {};
		self.__ObjList = {};
		self.__Logger = logging.getLogger("PPLT");

	def CreateSubClass(self, Name):
		# check if subclass allready exists:
		if self.__SubClassList.has_key(Name):
			# then return existing subclass
			return(self.__SubClassList.get(Name));
		# else create a new
		sub_class = ObjClassContainer(self, Name);
		self.__SubClassList.update( {Name:sub_class});	#add to table
		return(sub_class);
	
	def GetSubClass(self, Name):
		if self.__SubClassList.has_key(Name):
			return(self.__SubClassList.get(Name));
		return(None);
	
	def ListSubClasses(self):
		return(self.__SubClassList.keys());

	def ListItems(self):
		return(self.__ObjList.keys());

	def AddObject(self, Obj):
		# check type
		if not isinstance(Obj, DBObjBaseClass):
			return(False);
		# don't add a obj twice:
		#self.__Logger.debug("Adding obj %s"%Obj.GetName());
		if self.__ObjList.has_key(Obj.GetName()):
			old_obj = self.__ObjList.get(Obj.GetName());
			if old_obj.GetVersion()>Obj.GetVersion():	#replace newer packages
				self.__Logger.debug("Object %s already registered"%Obj.GetName());
				return(True);
		# else add:
		self.__ObjList.update( {Obj.GetName(): Obj} );
		return(True);

	def GetObject(self, Name):
		return(self.__ObjList.get(Name));

	def CheckConsistence(self):
		# search and destroy empty sub classes:
		for name in self.__SubClassList.keys():
			# tell this subclasse to check consistence
			self.__SubClassList[name].CheckConsistence();
			# if subclass is empty : remove
			if self.__SubClassList[name].IsEmpty():
				del self.__SubClassList[name];

		# search and destroy deleted devices/servers/coremodules
		for name in self.__ObjList.keys():
			if not self.__ObjList[name].FileExists():
				del self.__ObjList[name];
		# --- done ---
	
	def IsEmpty(self):
		# check if there are no 
		if len(self.__SubClassList.keys())==0 and len(self.__ObjList.kes())==0:
			return(True);
		return(False);

	def GetName(self):
		return(self.__Name);


class ObjRootClass(ObjClassContainer):
	def __init__(self):
		ObjClassContainer.__init__(self, None, None);
		self.__Logger = logging.getLogger("PPLT");

	def AddObject(self, Obj):
		# get attr:
		clist = Obj.GetClassList();

		# each Obj have to be a member of an class:
		if len(clist) == 0:
			self.__Logger.debug("Object %s have to be in a class"%Obj.GetName());
			return(False);

		pclass = self;
		# create all classes i need:
		for cname in clist:
			pclass = pclass.CreateSubClass(cname);
		# --- done ---
		#self.__Logger.debug("Obj added to %s"%pclass.GetName());
		return(pclass.AddObject(Obj));

	
	def GetObject(self, Name, ClassList):
		# a obj have to be member of (at least) one class
		if len(ClassList) == 0:
			return(None);

		pclass = self;
		for cname in ClassList:
			pclass = pclass.GetSubClass(cname);
			if not pclass:		# if class can not be found
				return(None);
		# --- done ---
		return(pclass.GetObject(Name));
	
	def ListClassesOf(self, ClassList):
		pclass = self;
		for cname in ClassList:
			#self.__Logger.debug("Try to list \"%s\""%cname);
			pclass = pclass.GetSubClass(cname);
			if not pclass:
				return(None);
		#self.__Logger.debug("List classes in %s"%pclass.GetName());
		return(pclass.ListSubClasses());

	def ListObjectsOf(self, ClassList):
		pclass = self;
		for cname in ClassList:
			pclass = pclass.GetSubClass(cname);
			if not pclass:
				return(None);
		return(pclass.ListItems());


class DataBase:
	def __init__(self, Path):
		self.__Devices = ObjRootClass();
		self.__Servers = ObjRootClass();
		self.__CoreMods= ObjRootClass();
		self.__Logger = logging.getLogger("PPLT");

		self.__SearchZIP(Path);
		self.__SearchXML(Path);

	def __SearchXML(self, Path):
		#self.__Logger.debug("Search %s..."%Path);
		Path = os.path.join(Path,"Mods");
		xml_list = glob.glob1(Path,'*.xml');

		for fname in xml_list:
			fname = Path+'/'+fname;
			try:
				#self.__Logger.debug("Try to process file \"%s\""%fname);
				obj = DBObjBaseClass(fname);
			except:
				self.__Logger.error("Can't process file \"%s\""%fname);
				continue;
			
			if not CheckCoreMods(self, obj.GetRequirements()):
				self.__Logger.error("Device/Server %s needs a cormod, can not be found"%(obj.GetName()));
				continue;
			if obj.GetType()==TYPE_SERVER:
				self.__Servers.AddObject(obj);
			if obj.GetType()==TYPE_DEVICE:
				self.__Devices.AddObject(obj);

	def __SearchZIP(self, Path, Class=[]):
		lst = os.listdir(Path);
		for item in lst:
			if os.path.isdir(os.path.join(Path,item)):
				self.__SearchZIP(os.path.join(Path,item),Class+[item]);
			elif os.path.isfile(os.path.join(Path,item)):
				if fnmatch.fnmatch(os.path.join(Path,item),"*.zip"):
					name = item.split(".");
					name = name[0];
					try:
						obj = DBCoreObjClass(os.path.join(Path,item),Class,name);
					except:
						self.__Logger.error("Error while process file %s"%os.path.join(Path,item));
						continue;
					self.__CoreMods.AddObject(obj);
				
	
	def GetDeviceFile(self, Name):
		lst = Name.split(".");
		devName = lst[-1];
		classList = lst[:-1];
		dev = self.__Devices.GetObject(devName, classList);
		if not dev:
			self.__Logger.warning("Device %s not found"%devName);
			return(None);
		return(dev.GetFileName());

	def GetServerFile(self, Name):
		lst = Name.split(".");
		serName = lst[-1];
		classList = lst[:-1];
		ser = self.__Servers.GetObject(serName, classList);
		if not ser:
			self.__Logger.warning("Server %s not found"%serName);
			return(None);
		return(ser.GetFileName());

	def GetServerVersion(self, Name):
		lst = Name.split(".");
		serName = lst[-1];
		classList = lst[:-1];
		ser = self.__Servers.GetObject(serName, classList);
		if not ser:
			self.__Logger.warning("Server %s not found"%serName);
			return(None);
		return(ser.GetVersion());

	def GetDeviceVersion(self, Name):
		lst = Name.split(".");
		serName = lst[-1];
		classList = lst[:-1];
		ser = self.__Devices.GetObject(serName, classList);
		if not ser:
			self.__Logger.warning("Device %s not found"%serName);
			return(None);
		return(ser.GetVersion());

	def ListServersIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		return(self.__Servers.ListObjectsOf(clist));

	def ListServerClassesIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		return(self.__Servers.ListClassesOf(clist));

	def ListDevicesIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		return(self.__Devices.ListObjectsOf(clist));

	def ListDeviceClassesIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		self.__Logger.debug("List classes in \"%s\""%ClassPath);
		return(self.__Devices.ListClassesOf(clist));

	def GetCoreModFile(self, Name):
		lst = Name.split(".");
		serName = lst[-1];
		classList = lst[:-1];
		#self.__Logger.debug("Try to find: %s in %s"%(serName,str(classList)));
		ser = self.__CoreMods.GetObject(serName, classList);
		if not ser:
			self.__Logger.warning("Coremod %s not found in %s"%(serName, str(classList)));
			return(None);
		return(ser.GetFileName());

	def GetCoreModVersion(self, Name):
		lst = Name.split(".");
		serName = lst[-1];
		classList = lst[:-1];
		ser = self.__CoreMods.GetObject(serName, classList);
		if not ser:
			self.__Logger.warning("Coremod %s not found"%serName);
			return(None);
		return(ser.GetVersion());

	def ListCoreModsIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		return(self.__CoreMods.ListObjectsOf(clist));

	def ListCoreModClassesIn(self, ClassPath=None):
		if not ClassPath: clist = [];
		else: clist = ClassPath.split('.');
		#self.__Logger.debug("List classes in \"%s\""%ClassPath);
		return(self.__CoreMods.ListClassesOf(clist));












def CheckCoreMods(DB, mods):
	for mod in mods:
		if not DB.GetCoreModFile(mod):
			return(False);
	return(True);
