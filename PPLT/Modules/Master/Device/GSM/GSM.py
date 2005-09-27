import GSMUtils;
import pyDCPU;
import struct;
import xdrlib;

class GSMAddress:
    def __init__(self, Type, Value):
        self.__Type  = Type;
        self.__Value = Value;
    def GetType(self):
        return(self.__Type);
    def GetValue(self):
        return(self.__Value);
    
NETWORK         = 1
BATTERY         = 2;
QUALITY         = 3;
ERRORRATE       = 4;
MANUFACTURER    = 10;
MODEL           = 11;
SMS             = 20;
ADDRHASH        = {'network':NETWORK,
                   'battery':BATTERY,
                   'quality':QUALITY,
                   'errorrate':ERRORRATE,
                   'manufacturer':MANUFACTURER,
                   'model':MODEL};


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup GSM")
        #try:
        #    if not GSMUtils.Reset(self.Connection):
        #        self.Logger.error("Error while reset mobile");
        #        return(False);
        return(True);
        #except:
        #    self.Logger.error("Error while reset mobile");
        #    return(False);
        #return(False);


    def connect(self, AddrStr):
        if not AddrStr:
            self.Logger.error("Need Address for connection");
            return(None);

        if AddrStr.find('sms:')==0:
            tmp = AddrStr.split(':');
            if not len(tmp) == 2:
                self.Logger.error("InvalidFormat: %s"%AddrStr);
                return(None);
            Addr = GSMAddress(SMS, tmp[1]);
            Con = pyDCPU.MasterConnection(self, Addr);
            self.Logger.debug("SMS destination: %s"%str(tmp[1]));
        elif ADDRHASH.has_key(AddrStr):
            Addr = GSMAddress(ADDRHASH[AddrStr],None);
            Con = pyDCPU.MasterConnection(self, Addr);
        else:
            self.Logger.error("Invalid Addressformat %s"%AddrStr);
            Con = None;
        return(Con);



    def read(self, Connection, Len):
        if not isinstance(Connection, pyDCPU.MasterConnection):
            self.Logger.error("No connection to me???");
            raise pyDCPU.FatIOModError;

        if Connection.Address.GetType() == BATTERY:
            try:
                s = GSMUtils.GetBattery(self.Connection);
            except:
                self.Logger.error("IO Error while get battery")
                raise pyDCPU.IOModError;

            if not s:
                self.Logger.error("Error while get battery status");
                raise pyDCPU.IOModError;
            self.Logger.debug("Battery: %s"%s);
            packer = xdrlib.Packer();
            packer.pack_uint(int(s));
            return packer.get_buffer();

        elif Connection.Address.GetType() == NETWORK:
            try:
                s = GSMUtils.GetNetwork(self.Connection);
            except:
                self.Logger.error("Error while get network status");
                raise pyDCPU.IOModError;
            if not s:
                self.Logger.error("GetNetwork returned NULL");
                raise pyDCPU.IOModError;
            if len(s)<2:
                self.Logger.error("invalid format");
                raise pyDCPU.IOModError;
            self.Logger.debug("Network status %s"%s[1]);
            packer = xdrlib.Packer();
            packer.pack_uint(int(s[1]));
            return packer.get_buffer();
        
        elif Connection.Address.GetType() == QUALITY:
            self.Logger.debug("Get quality of service");
            try:
                s = GSMUtils.GetQuality(self.Connection);
            except:
                self.Logger.error("Error while get quality");
                raise pyDCPU.IOModError;
            if not s:
                self.Logger.error("GetQuality returned NULL");
                raise IOModError;
            self.Logger.debug("Quality %s"%str(s));
            if len(s) != 2:
                self.Logger.error("Invalid format returned: %s"%s);
                raise IOModError;
            packer = xdrlib.Packer();
            packer.pack_uint(int(s[0]));
            return packer.get_buffer();
        
        elif Connection.Address.GetType() == ERRORRATE:
            try:
                s = GSMUtils.GetQuality(self.Connection);
            except:
                self.Logger.error("Error while get quality");
                raise pyDCPU.IOModError;
            if not s:
                self.Logger.error("GetQuality returned NULL");
                raise IOModError;
            if len(s) != 2:
                self.Logger.error("Invalid format returned");
                raise IOModError;
            packer = xdrlib.Packer();
            packer.pack_uint(int(s[1]));
            return packer.get_buffer();
        
        elif Connection.Address.GetType() == MANUFACTURER:
            try:
                s = GSMUtils.GetManufacturer(self.Connection);
                packer = xdrlib.Packer();
                packer.pack_string(s);
                return packer.get_buffer();
            except Exception, e:
                self.Logger.error("Error while get manufacturer string: %s"%str(e));
                raise pyDCPU.IOModError;
        
        elif Connection.Address.GetType() == MODEL:
            try:
                s = GSMUtils.GetModel(self.Connection);
                packer = xdrlib.Packer();
                packer.pack_string(s);
                return packer.get_buffer();
            except:
                self.Logger.error("Error while get model name");
                raise IOModError;
        
        elif Connection.Address.GetType() == SMS:
            self.Logger.error("Send SMS is Write-Only");
            raise pyDCPU.IOModError;
        
        else:
            self.Logger.error("Invalid chanel address %s"%str(Connection.Address.GetType()));
            raise pyDCPU.FatIOModError;
        


    def write(self, Connection, Data):
        self.Logger.debug("write...");
        unpacker = xdrlib.Unpacker(Data);
        Msg = unpacker.unpack_string();
        unpacker.done()
        self.Logger.debug("Send sms...");
        if Connection.Address.GetType() == SMS:
            Dest = Connection.Address.GetValue();
            try:
                ret = GSMUtils.SendSMS(self.Connection, Dest, Msg);
            except:
                self.Logger.error("Error while send SMS");
                raise pyDCPU.IOModError;
            if not ret:
                self.Logger.error("Error while send SMS (errorcode returned by phone)");
                raise(pyDCPU.IOModError);
            return(len(Data));
        else:
            self.Logger.error("Invalid chanel Address");
            raise pyDCPU.IOModError;
        return(None);
