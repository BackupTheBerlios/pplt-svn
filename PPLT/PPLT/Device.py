import logging;
import DeviceDescription;
import Exceptions;
import pyDCPU;


class Device:
	def __init__(self, CoreObject, FileName, Parameters):
		""" This is the Device Object for the PPLT system. 
 It parse the given device-decription-file load all pyDCPU modules
 descibed."""
		#save core object
		self.__CoreObject = CoreObject;
		# get logger
		self.__Logger = logging.getLogger('PPLT');
		self.__SlotTable = {};
 
		# load setupdescription from file...
		self.__Setup = DeviceDescription.LoadSetup(FileName);
		if not self.__Setup:
			self.__Logger.error("Unable to load file \"%s\"."%FileName);
			raise Exception('Unable to load file \"%s\"'%FileName);
        
		# just do it...
		if not self.__Setup.DoSetup(self.__CoreObject, Parameters):
			self.__Logger.error("Error while setup device of file \"%s\""%FileName);
			self.destroy()
			raise Exception('Error whiel setup device of file "%s"'%FileName);


	def destroy(self):
		""" This method will destroy a instance of this class """
		if len(self.__SlotTable.keys())>0:
			self.__Logger.warning("Can't unload. Symbols are attached to this device!");
			return(False);
		return(self.__Setup.Unload());
        

	def register(self, NameSpace, Address, Type, TimeOut=0.5):
		""" Will bind a Symbol to NameSpace::Address """
		# get deviceID by namespace:
		ObjID = self.__Setup.GetObjByNameSpace(NameSpace);
		if not ObjID:
			self.__Logger.error("No Namespace \"%s\" in this device"%NameSpace);
			return(None);

		# create symbol slot:
		SlotID = self.__CoreObject.MasterTreeAttachSymbolSlot(ObjID, Address, Type, TimeOut);
		if not SlotID:
			self.__Logger.error("Error while create SymbolSlot for %s"%Address);
			return(None);
		
		# save in Address->SySl Table
		if not self.__SlotTable.has_key(SlotID):
			self.__SlotTable.update( {SlotID:0} );
		self.__SlotTable[SlotID] = self.__SlotTable[SlotID]+1;
		return(SlotID);
	

	def unregister(self, SlotID):
		""" Unregister a Symbol """
		# check id Slot is attached to this device:
		if not self.__SlotTable.has_key(SlotID):
			self.__Logger.error("No slot with this id is attached to this device!");
			return(False);
		
		# reduce usage-counter for slot:
		self.__SlotTable[SlotID] = self.__SlotTable[SlotID] -1;
		# if slot is unused -> remove it:
		if self.__SlotTable[SlotID] < 1:
			del self.__SlotTable[SlotID];
			return(self.__CoreObject.MasterTreeDel(SlotID));
		return(True);

