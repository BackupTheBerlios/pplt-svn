import GSMSMS;
import logging;
import readline;

def Reset(Con):
    Con.flush();
    Con.write("ATZ\r\n");
    readline.read(Con,"\r\n");
    readline.read(Con,"\r\n");
    if readline.read(Con,"\r\n") == 'OK':
        Con.flush();
        return(True);
    return(False);

def GetServiceCenter(Con):
    Con.flush();
    Con.write('AT+CSCA?\r\n');
    readline.read(Con,"\r\n");          # get echo ...
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");          # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    if -1 == tmp.find('"'):
        return(None);
    sc = tmp.split('"')[1];
    return("\"%s\""%sc);

def GetManufacturer(Con):
    Con.write('AT+CGMI\r\n');
    readline.read(Con,"\r\n");      # get echo
    s = readline.read(Con,"\r\n");
    if s == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    return(s);

def GetModel(Con):
    Con.write('AT+CGMM\r\n');
    readline.read(Con,"\r\n");      # get echo
    s = readline.read(Con,"\r\n");
    if s == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");      # get empty line;
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    return(s);
    
def GetQuality(Con):
    Con.write('AT+CSQ\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    tq = tmp.split(' ')[1];
    q = tq.split(',');
    return(q);

def GetBattery(Con):
    Con.write('AT+CBC\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    tq = tmp.split(' ')[1];
    q = tq.split(',')[1];
    return(q);

def GetNetwork(Con):
    Con.write('AT+CREG?\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR':
        return(None);
    readline.read(Con,"\r\n");      # read empty line;
    if not readline.read(Con,"\r\n") == 'OK':
        return(None);
    tq = tmp.split(' ');
    if len(tq)>1:
        q = tq[1].split(',');
    else:
        return(None);
    return(q);

def SendSMS(Con, Dest, Msg):
    logger = logging.getLogger("pyDCPU");
    sms = GSMSMS.PDUSMS(Dest,Msg);
    data = sms.SMSToHex();

    if not data:
        return(False);
    logger.debug("SMSPDU(hex): %s"%data);
    Con.write("AT+CMGS=%i\r%s\x1A"%(int(len(data)/2)-1,data));
    logger.debug("SMS \"%s\" send..."%Msg);
    readline.read(Con,"\r\n"); #get echo
    readline.read(Con,"\r\n"); 
    tmp = readline.read(Con,"\r\n");
    logger.debug("Phone returned: %s"%str(tmp));
    if not 0 == tmp.find('+CMGS:'):
        logger.error("Error while send sms to %s: %s"%(Dest,tmp));
        return(False);

    return(True);
